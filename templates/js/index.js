$("#submit").click(function(){
    console.log("sdd");
    $("#divcard").append(createCard());
}); 

function createCard(title, article, link){
    return '<div class="col-xs-6 well"id="divcard"><div class="caption"><h3>'+ title +'</h3><div class="card bg-light"><div class="card-body"><p class="card-text well">' + article + '</p></div></div><p><a href=""class="btn btn-primary" role="button"id="link">Button</a></p></div></div>'
} 
