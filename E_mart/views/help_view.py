from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required
from E_mart.models import Help
import json
from E_mart.services import (
    ContactService, 
    HelpService, 
    FAQService, 
    DashboardService,
    chatbot_manager
)


@method_decorator(enduser_required, name='dispatch')
class ContactPageView(View):
    """Render the contact page with all necessary data"""
    
    def get(self, request):
        context = {}
        
        try:
            # Get user's help problems if authenticated
            if request.user.is_authenticated:
                help_data = HelpService.get_user_help_problems(request.user)
                context['help_problems'] = help_data['problems']
                context['pending_count'] = help_data['pending_count']
                context['in_progress_count'] = help_data['in_progress_count']
                context['resolved_count'] = help_data['resolved_count']
            else:
                context['help_problems'] = []
                context['pending_count'] = 0
                context['in_progress_count'] = 0
                context['resolved_count'] = 0
            
            # Get active FAQs
            faqs = FAQService.get_faqs(limit=6)
            context['faqs'] = faqs
            
            # Get user's recent contact queries if needed
            if request.user.is_authenticated and request.user.email:
                contact_data = ContactService.get_user_contact_queries(request.user)
                context['recent_queries'] = contact_data['queries']
            
        except Exception as e:
            # Log error if needed
            print(f"Error loading contact page: {e}")
            context['help_problems'] = []
            context['faqs'] = []
            context['pending_count'] = 0
            context['in_progress_count'] = 0
            context['resolved_count'] = 0
        
        return render(request, 'enduser/contact_page.html', context)


@method_decorator(enduser_required, name='dispatch')
class SubmitContactQuery(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Use service to create contact message
            message = ContactService.create_contact_message(
                user=request.user,
                data=data,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Send acknowledgment email
            ContactService.send_acknowledgment_email(message)
            
            return JsonResponse({
                'success': True,
                'message': 'Your query has been submitted successfully',
                'ticket_id': message.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class GetContactQueries(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            # Use service to get contact queries
            contact_data = ContactService.get_user_contact_queries(
                user=request.user,
                is_staff=request.user.is_staff
            )
            
            queries_data = [{
                'id': q.id,
                'name': q.name,
                'subject': q.subject,
                'status': q.get_status_display(),
                'status_code': q.status,
                'created_at': q.created_at.strftime('%Y-%m-%d %H:%M')
            } for q in contact_data['queries']]
            
            return JsonResponse({
                'success': True,
                'queries': queries_data,
                'pending_count': contact_data['pending_count'],
                'resolved_count': contact_data['resolved_count']
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class GetHelpProblems(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            # Use service to get help problems
            help_data = HelpService.get_user_help_problems(request.user)
            
            # Format problems data
            problems_data = [{
                'id': p.id,
                'order_id': p.order_item.order.id if p.order_item and hasattr(p.order_item, 'order') else 'N/A',
                'product_name': p.order_item.product.name if p.order_item else 'Unknown',
                'problem': p.problem,
                'status': p.status,
                'status_display': p.get_status_display(),
                'reported_at': p.reported_at.strftime('%Y-%m-%d %H:%M'),
                'priority': p.priority,
                'admin_response': p.admin_response
            } for p in help_data['problems']]
            
            return JsonResponse({
                'success': True,
                'problems': problems_data,
                'problem_counts': {
                    'Pending': help_data['pending_count'],
                    'In Progress': help_data['in_progress_count'],
                    'Resolved': help_data['resolved_count']
                },
                'pending_count': help_data['pending_count'],
                'in_progress_count': help_data['in_progress_count'],
                'resolved_count': help_data['resolved_count'],
                'total': help_data['total']
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class SubmitHelpProblem(View):
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Please login to report a problem'
                }, status=401)
            
            data = json.loads(request.body)
            
            # Use service to create help problem
            problem = HelpService.create_help_problem(request.user, data)
            
            return JsonResponse({
                'success': True,
                'message': 'Problem reported successfully',
                'problem_id': problem.id,
                'status': problem.get_status_display()
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class UpdateHelpProblemStatus(View):
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            data = json.loads(request.body)
            problem = get_object_or_404(Help, id=data.get('problem_id'))
            
            # Check permissions
            if not request.user.is_staff and problem.user != request.user:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied'
                }, status=403)
            
            # Use service to update status
            problem = HelpService.update_problem_status(problem, data.get('status'))
            
            return JsonResponse({
                'success': True,
                'message': 'Status updated successfully',
                'new_status': problem.get_status_display()
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class GetHelpProblemDetail(View):
    def get(self, request, problem_id):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            problem = get_object_or_404(Help, id=problem_id)
            
            # Check permissions
            if not request.user.is_staff and problem.user != request.user:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied'
                }, status=403)
            
            # Use service to format problem data
            problem_data = HelpService.format_problem_data(problem)
            
            return JsonResponse({
                'success': True,
                'problem': problem_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class GetFAQs(View):
    def get(self, request):
        try:
            category = request.GET.get('category')
            search = request.GET.get('search')
            
            # Use service to get FAQs
            faqs = FAQService.get_faqs(category=category, search=search)
            
            # Format FAQ data
            faqs_data = FAQService.format_faq_data(faqs)
            
            return JsonResponse({
                'success': True,
                'faqs': faqs_data,
                'count': len(faqs_data)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class GetDashboardStats(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            # Use service to get stats based on user role
            if request.user.is_staff:
                stats = DashboardService.get_admin_stats()
            else:
                stats = DashboardService.get_user_stats(request.user)
            
            return JsonResponse({
                'success': True,
                'stats': stats
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


class SendChatMessage(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Get or create session
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            
            # Use chatbot manager to process message
            bot_response = chatbot_manager.process_message(
                message=data.get('message'),
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id
            )
            
            # Save messages to database
            bot_message = chatbot_manager.save_chat_messages(
                session_id=session_id,
                user_message=data.get('message'),
                bot_response=bot_response,
                user=request.user if request.user.is_authenticated else None
            )
            
            return JsonResponse({
                'success': True,
                'user_message': data.get('message'),
                'bot_response': bot_response,
                'timestamp': bot_message.created_at.strftime('%H:%M')
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)