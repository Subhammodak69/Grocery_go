# services.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from E_mart.models import Help, ContactMessage, FAQ, ChatMessage, Order
import json
from typing import Dict, Any, Optional, List
from django.db.models import QuerySet

class ContactService:
    """Service class for contact-related operations"""
    
    @staticmethod
    def create_contact_message(user, data: Dict[str, Any], ip_address: str) -> ContactMessage:
        """Create a new contact message"""
        return ContactMessage.objects.create(
            user=user if user and user.is_authenticated else None,
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone', ''),
            subject_type=data.get('subject_type'),
            subject=data.get('subject'),
            message=data.get('message'),
            ip_address=ip_address
        )
    
    @staticmethod
    def send_acknowledgment_email(message: ContactMessage) -> None:
        """Send acknowledgment email for contact query"""
        subject = "Thank you for contacting GroceryGo"
        email_body = f"""
        Dear {message.name},
        
        Thank you for reaching out to us. We have received your query and will get back to you within 24 hours.
        
        Your Ticket ID: #{message.id}
        Subject: {message.subject}
        
        Best regards,
        GroceryGo Support Team
        """
        
        send_mail(
            subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [message.email],
            fail_silently=True
        )
    
    @staticmethod
    def get_user_contact_queries(user, is_staff: bool = False, limit: int = 10) -> Dict[str, Any]:
        """Get contact queries for user or all if staff"""
        if is_staff:
            queries = ContactMessage.objects.all().order_by('-created_at')[:limit]
            pending_count = ContactMessage.objects.filter(status=1).count()
            resolved_count = ContactMessage.objects.filter(status=3).count()
        else:
            queries = ContactMessage.objects.filter(email=user.email).order_by('-created_at')[:5]
            pending_count = queries.filter(status=1).count()
            resolved_count = queries.filter(status=3).count()
        
        return {
            'queries': queries,
            'pending_count': pending_count,
            'resolved_count': resolved_count
        }


class HelpService:
    """Service class for help/problem-related operations"""
    
    @staticmethod
    def get_user_help_problems(user, limit: int = 10) -> Dict[str, Any]:
        """Get help problems for a user with counts"""
        problems = Help.objects.filter(
            user=user, 
            is_active=True
        ).select_related(
            'order_item__order', 
            'order_item__product'
        )
        
        return {
            'problems': problems.order_by('-reported_at')[:limit],
            'pending_count': problems.filter(status=1).count(),
            'in_progress_count': problems.filter(status=2).count(),
            'resolved_count': problems.filter(status=3).count(),
            'total': problems.count()
        }
    
    @staticmethod
    def create_help_problem(user, data: Dict[str, Any]) -> Help:
        """Create a new help problem"""
        return Help.objects.create(
            user=user,
            order_item_id=data.get('order_item_id'),
            problem=data.get('problem'),
            status=1,  # Pending
            priority=data.get('priority', 1),
            is_active=True
        )
    
    @staticmethod
    def update_problem_status(problem: Help, status: int) -> Help:
        """Update problem status"""
        problem.status = status
        if status == 3:  # Resolved
            problem.resolved_at = timezone.now()
        problem.save()
        return problem
    
    @staticmethod
    def format_problem_data(problem: Help) -> Dict[str, Any]:
        """Format problem data for API response"""
        return {
            'id': problem.id,
            'user': problem.user.username,
            'user_email': problem.user.email,
            'order_item': {
                'id': problem.order_item.id,
                'product': problem.order_item.product.name if problem.order_item else None,
                'quantity': problem.order_item.quantity if problem.order_item else None,
                'price': float(problem.order_item.price) if problem.order_item else None
            } if problem.order_item else None,
            'problem': problem.problem,
            'status': problem.get_status_display(),
            'status_code': problem.status,
            'reported_at': problem.reported_at.strftime('%Y-%m-%d %H:%M'),
            'resolved_at': problem.resolved_at.strftime('%Y-%m-%d %H:%M') if problem.resolved_at else None,
            'admin_response': problem.admin_response,
            'priority': problem.priority,
            'is_active': problem.is_active
        }


class FAQService:
    """Service class for FAQ-related operations"""
    
    @staticmethod
    def get_faqs(category: Optional[str] = None, search: Optional[str] = None, limit: int = 10) -> QuerySet:
        """Get FAQs with optional filters"""
        faqs = FAQ.objects.filter(is_active=True)
        
        if category:
            faqs = faqs.filter(category=category)
        
        if search:
            faqs = faqs.filter(
                models.Q(question__icontains=search) |
                models.Q(answer__icontains=search)
            )
        
        return faqs.order_by('category', 'order')[:limit]
    
    @staticmethod
    def format_faq_data(faqs: QuerySet) -> List[Dict[str, Any]]:
        """Format FAQ data for API response"""
        return [{
            'id': f.id,
            'question': f.question,
            'answer': f.answer,
            'category': f.get_category_display(),
            'category_code': f.category
        } for f in faqs]


class DashboardService:
    """Service class for dashboard statistics"""
    
    @staticmethod
    def get_admin_stats() -> Dict[str, int]:
        """Get admin dashboard statistics"""
        return {
            'total_help_problems': Help.objects.filter(is_active=True).count(),
            'pending_help': Help.objects.filter(status=1, is_active=True).count(),
            'in_progress_help': Help.objects.filter(status=2, is_active=True).count(),
            'resolved_help': Help.objects.filter(status=3, is_active=True).count(),
            'total_contact_queries': ContactMessage.objects.count(),
            'pending_queries': ContactMessage.objects.filter(status=1).count(),
            'resolved_queries': ContactMessage.objects.filter(status=3).count(),
        }
    
    @staticmethod
    def get_user_stats(user) -> Dict[str, int]:
        """Get user dashboard statistics"""
        return {
            'total_help_problems': Help.objects.filter(user=user, is_active=True).count(),
            'pending_help': Help.objects.filter(user=user, status=1, is_active=True).count(),
            'in_progress_help': Help.objects.filter(user=user, status=2, is_active=True).count(),
            'resolved_help': Help.objects.filter(user=user, status=3, is_active=True).count(),
        }


class ChatbotManager:
    """
    Manages chatbot conversations with context memory
    """
    
    def __init__(self):
        self.conversation_history = {}
    
    def get_context_key(self, user, session_id):
        """Generate unique key for conversation context"""
        if user and user.is_authenticated:
            return f"user_{user.id}"
        return f"session_{session_id}"
    
    def get_conversation_context(self, context_key):
        """Get conversation history for a user/session"""
        if context_key not in self.conversation_history:
            self.conversation_history[context_key] = {
                'history': [],
                'last_intent': None,
                'awaiting_details': False
            }
        return self.conversation_history[context_key]
    
    def save_chat_messages(self, session_id, user_message, bot_response, user=None):
        """Save chat messages to database"""
        # Save user message
        ChatMessage.objects.create(
            user=user if user and user.is_authenticated else None,
            session_id=session_id,
            message=user_message,
            is_bot=False
        )
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            session_id=session_id,
            message=bot_response,
            is_bot=True
        )
        
        return bot_message
    
    def process_message(self, message, user=None, session_id=None):
        """
        Process message with context awareness
        """
        context_key = self.get_context_key(user, session_id)
        context = self.get_conversation_context(context_key)
        
        # Add message to history
        context['history'].append({
            'role': 'user',
            'message': message,
            'timestamp': timezone.now()
        })
        
        # Check if we're in a multi-turn conversation
        if context['awaiting_details']:
            response = self.handle_follow_up(message, context)
        else:
            response = self.get_bot_response(message, user, context)
        
        # Add response to history
        context['history'].append({
            'role': 'bot',
            'message': response,
            'timestamp': timezone.now()
        })
        
        # Keep history manageable (last 10 messages)
        if len(context['history']) > 10:
            context['history'] = context['history'][-10:]
        
        return response
    
    def handle_follow_up(self, message, context):
        """Handle follow-up messages in a conversation"""
        last_intent = context.get('last_intent')
        
        if last_intent == 'order_tracking':
            # Extract order ID from message
            import re
            order_id_match = re.search(r'\d+', message)
            if order_id_match:
                return f"I'll help you track order #{order_id_match.group()}. You can see real-time updates in the 'My Orders' section."
            else:
                return "Please provide your order ID number so I can help track it."
        
        elif last_intent == 'complaint':
            context['awaiting_details'] = False
            return "Thank you for providing the details. Our support team will look into this and contact you within 24 hours."
        
        # Reset awaiting flag
        context['awaiting_details'] = False
        return self.get_bot_response(message, None, context)
    
    def get_bot_response(self, message, user, context):
        """
        Enhanced bot response system with context awareness and better relevance
        """
        message_lower = message.lower().strip()
        
        # Common greeting patterns
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
        if any(greet in message_lower for greet in greetings):
            if user and user.is_authenticated:
                return f"Hello {user.first_name}! 👋 How can I assist you with your grocery shopping today?"
            return "Hello! 👋 Welcome to GroceryGo. How can I help you today?"
        
        # Order related queries
        if any(word in message_lower for word in ['order', 'orders', 'my order']):
            if 'track' in message_lower or 'status' in message_lower or 'where' in message_lower:
                if user and user.is_authenticated:
                    # Check if user has recent orders
                    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:3]
                    if recent_orders.exists():
                        response = "📦 Your recent orders:\n"
                        for order in recent_orders:
                            response += f"• Order #{order.id}: {order.get_status_display()} - {order.created_at.strftime('%d %b')}\n"
                        response += "\nVisit 'My Orders' section for detailed tracking."
                        return response
                return "To track your order, please visit the 'My Orders' section. You'll find real-time tracking updates there."
            
            elif 'cancel' in message_lower:
                return "⚠️ To cancel an order, please go to 'My Orders' and select the order you wish to cancel. Cancellation is only possible within 5 minutes of placing the order."
            
            elif 'change' in message_lower or 'modify' in message_lower:
                return "📝 Order modifications can be made within 5 minutes of placing the order. Please visit 'My Orders' section or contact our support team immediately."
        
        # Product related queries
        if any(word in message_lower for word in ['product', 'item', 'groceries', 'available']):
            if 'search' in message_lower:
                # Extract potential search term
                words = message_lower.split()
                for i, word in enumerate(words):
                    if word == 'search' and i + 1 < len(words):
                        search_term = words[i + 1]
                        return f"🔍 Looking for '{search_term}'? You can search for it directly in the search bar above. We have a wide range of fresh groceries!"
            
            if 'price' in message_lower or 'cost' in message_lower:
                return "💰 You can check product prices directly on the product page. We offer competitive prices and regular discounts!"
            
            if 'available' in message_lower:
                return "🛒 We have thousands of products available! From fresh fruits & vegetables to dairy, bakery, and household essentials. Browse our categories to explore."
        
        # Delivery related queries
        if any(word in message_lower for word in ['delivery', 'shipping', 'deliver', 'arrive', 'reach']):
            if 'time' in message_lower or 'how long' in message_lower:
                return "⏰ We deliver within 2 hours in most areas! You'll receive real-time tracking updates via SMS once your order is confirmed."
            
            if 'free' in message_lower:
                return "🚚 Free delivery is available on orders above ₹499. For orders below ₹499, a nominal delivery fee of ₹40 applies."
            
            if 'area' in message_lower or 'location' in message_lower or 'pincode' in message_lower:
                return "📍 Enter your pincode on the homepage to check if we deliver to your area. We currently serve 50+ cities across India!"
            
            if 'slot' in message_lower or 'schedule' in message_lower:
                return "📅 You can choose your preferred delivery slot during checkout. Same-day delivery slots are available if you order before 8 PM."
        
        # Return/Refund related queries
        if any(word in message_lower for word in ['return', 'refund', 'replacement', 'exchange']):
            if 'policy' in message_lower:
                return "📋 Our return policy: Items can be returned within 24 hours of delivery if damaged or incorrect. Refunds are processed within 3-5 business days."
            
            if 'how to' in message_lower or 'process' in message_lower:
                return "🔄 To initiate a return: Go to 'My Orders' > Select the order > Click on 'Return/Replace'. Follow the instructions or contact our support team."
            
            if 'money back' in message_lower or 'get my money' in message_lower:
                return "💰 Refunds are credited to your original payment method within 3-5 business days. UPI payments are typically faster (24-48 hours)."
        
        # Payment related queries
        if any(word in message_lower for word in ['payment', 'pay', 'cod', 'card', 'upi']):
            if 'method' in message_lower or 'ways' in message_lower or 'options' in message_lower:
                return "💳 We accept multiple payment methods:\n• Credit/Debit Cards\n• UPI (Google Pay, PhonePe, Paytm)\n• Net Banking\n• Cash on Delivery (COD)\n• Wallet"
            
            if 'secure' in message_lower or 'safe' in message_lower:
                return "🔒 All payments are 100% secure. We use industry-standard encryption to protect your payment information."
            
            if 'cash on delivery' in message_lower or 'cod' in message_lower:
                return "💵 Cash on Delivery is available for orders up to ₹5000. You can pay by cash or digital payment at your doorstep."
            
            if 'failed' in message_lower or 'problem' in message_lower:
                return "⚠️ If your payment failed, don't worry - your account won't be charged. Please try again or use a different payment method. If money was deducted, it will be refunded automatically within 3-5 days."
        
        # Account related queries
        if any(word in message_lower for word in ['account', 'profile', 'login', 'signup', 'password', 'forgot']):
            if 'create' in message_lower or 'new' in message_lower or 'sign up' in message_lower:
                return "📝 Creating an account is easy! Click on 'Login/Signup' at the top right corner and follow the instructions. You'll get exclusive offers and faster checkout!"
            
            if 'forgot password' in message_lower:
                return "🔐 Click on 'Login' > 'Forgot Password' and follow the instructions sent to your email to reset your password."
            
            if 'update' in message_lower or 'change' in message_lower:
                return "✏️ You can update your profile information in the 'My Account' section after logging in."
        
        # Contact/Support queries
        if any(word in message_lower for word in ['contact', 'support', 'help', 'human', 'agent', 'speak', 'talk']):
            return """📞 We're here to help! Here's how you can reach us:

📧 Email: support@grocerygo.com (24/7)
📞 Phone: +91 98765 43210 (9 AM - 8 PM, Mon-Sat)
💬 Live Chat: Click the chat button anytime

Average response time: 2 hours for email, 2 minutes for chat during business hours."""
        
        # Offers and Discounts
        if any(word in message_lower for word in ['offer', 'discount', 'coupon', 'promo', 'deal']):
            return """🎉 Current Offers:

• First order: 20% off (upto ₹100) - Use code: WELCOME20
• Free delivery on orders above ₹499
• Weekly specials on fresh produce
• Buy 2 Get 1 Free on select items

Check the 'Offers' section for more exciting deals!"""
        
        # Store/Timing queries
        if any(word in message_lower for word in ['store', 'timing', 'open', 'close', 'hour']):
            return "🕒 We're open 24/7! You can place orders anytime. Delivery slots are available from 7 AM to 11 PM daily."
        
        # Technical issues
        if any(word in message_lower for word in ['error', 'issue', 'problem', 'not working', 'bug', 'glitch']):
            return "🛠️ We apologize for the inconvenience. Please try refreshing the page or clearing your browser cache. If the issue persists, contact our technical team at tech@grocerygo.com"
        
        # Feedback/Suggestions
        if any(word in message_lower for word in ['feedback', 'suggestion', 'improve', 'idea']):
            return "💡 We value your feedback! Please share your suggestions at feedback@grocerygo.com. Your input helps us improve!"
        
        # Default response with helpful options
        return """Thank you for reaching out to GroceryGo! 🌟

I can help you with:
• 📦 Order tracking & status
• 🚚 Delivery information
• 💳 Payment options
• 🔄 Returns & refunds
• 📝 Account help
• 🎉 Offers & discounts

What would you like to know more about?"""


# Initialize chatbot manager instance
chatbot_manager = ChatbotManager()
