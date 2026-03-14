async function poster_update(){

const messageEl=document.getElementById('message');

messageEl.textContent='';
messageEl.className='message';

const posterId=document.getElementById('poster_id').value;
const product_id=document.getElementById('product_id').value;
const title=document.getElementById('title').value.trim();
const description=document.getElementById('description').value.trim();
const file=document.getElementById('image').files[0];
const start_date=document.getElementById('start_date').value;
const end_date=document.getElementById('end_date').value;

if(!product_id || !title || !start_date || !end_date){

messageEl.textContent='Please fill all required fields';
messageEl.classList.add('error');

return;

}

const formData=new FormData();

formData.append('product_id',product_id);
formData.append('title',title);
formData.append('description',description);

if(file){
formData.append('image',file);
}

formData.append('start_date',start_date);
formData.append('end_date',end_date);

try{

const response=await fetch(`/admin/poster/update/${posterId}/`,{

method:'POST',
credentials:'include',
body:formData

});

if(!response.ok){

const errorData=await response.json();
throw new Error(errorData.error || 'Failed to update poster');

}

messageEl.textContent='Poster updated successfully! Redirecting...';
messageEl.classList.add('success');

setTimeout(()=>{

window.location.href='/admin/posters/';

},1000);

}

catch(err){

messageEl.textContent=err.message;
messageEl.classList.add('error');

}

}
