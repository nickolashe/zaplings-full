$(document).ready(function() {
    var loveNum = 12;
    $('body').one('click',function(){
    
    var count=30;
    var counter=setInterval(timer, 1000); //1000 will  run it every 1 second

    function timer()
    {
      count=count-1;
      $('#timer').attr("style", "color: #70bf4f");
      if (count < 0)
      {
         clearInterval(counter);
         $('.continue-delay').removeClass('hidden');
         return;
      };

      document.getElementById("timer").innerHTML=count; // watch for spelling
    };
  });
});

