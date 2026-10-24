/* Contact form: opens the visitor's email app with a prepared message to Markov's. */
(function(){
  const EMAIL='workwithmarkov@gmail.com';
  const form=$('#cform');if(!form)return;
  const out=$('#cout');
  const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const topic=$('#ct');
  /* ?topic=creator on the URL preselects the creator option */
  try{const q=new URLSearchParams(location.search).get('topic');if(q&&topic){const o=[...topic.options].find(x=>x.dataset.key===q);if(o)topic.value=o.value}}catch(e){}
  form.addEventListener('submit',e=>{
    e.preventDefault();
    const name=$('#cn').value.trim(),brand=$('#cb').value.trim(),goal=$('#cg').value.trim(),kind=topic?topic.value:'Campaign enquiry';
    const contactBack=$('#cr')?$('#cr').value.trim():'';
    const subject=`${kind}${brand?': '+brand:''}`;
    const body=`Hello Markov's team,\n\n${goal}\n\nName: ${name}\n${kind.startsWith('Creator')?'Channel or handle':'Brand'}: ${brand}${contactBack?'\nReply to: '+contactBack:''}\n`;
    const href=`mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    out.innerHTML=`<b>Opening your email app.</b> If nothing opens, write to <a href="mailto:${EMAIL}"><b>${EMAIL}</b></a> or <button type="button" class="linkbtn" data-copy="${esc(`To: ${EMAIL}\nSubject: ${subject}\n\n${body}`)}">copy the message</button>.`;
    window.location.href=href;
  });
})();
