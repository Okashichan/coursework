let scroller = document.querySelector('#scroller');
let template = document.querySelector('#post_template');
let sentinel = document.querySelector('#sentinel');

let counter = 0;

function loadItems(){
    fetch('/post-load?c='+counter).then((response) => {
        response.json().then((data) => {
            if(!data.length || data[0]){
                sentinel.innerHTML = '';
            }
            console.log(data)
    
            for(let i=0;i<data.length;i++){
                let template_clone = template.content.cloneNode(true);
                template_clone.querySelector('#post_id').href+=data[i][0];
                template_clone.querySelector('#head').innerHTML = data[i][1];
                template_clone.querySelector('#data').innerHTML = data[i][2];
                template_clone.querySelector('#date').innerHTML = data[i][3];
                template_clone.querySelector('#user_id').href+=data[i][4];
                template_clone.querySelector('#user_id').innerHTML+=data[i][4];
                scroller.appendChild(template_clone);
                counter+=1;
            }
        })
    })
}

var intersectionObserver = new IntersectionObserver(entries => {

    if (entries[0].intersectionRatio <= 0) {
      return;
    }
  
    loadItems();
  
  });

intersectionObserver.observe(sentinel);