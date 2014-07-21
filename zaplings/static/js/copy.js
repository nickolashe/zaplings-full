var client = new ZeroClipboard( document.getElementById("copy-link") );

client.on( "ready", function( readyEvent ) {
  // alert( "ZeroClipboard SWF is ready!" );

  client.on( "aftercopy", function( event ) {
    // `this` === `client`
    // `event.target` === the element that was clicked
    //event.target.style.display = "none";
    var button = $("#copy-link");
  	button.data("text-original", button.text());
  	button.text(button.data("text-swap"));
  } );
} );