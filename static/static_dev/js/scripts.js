$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    form.on('submit', function(e){
       e.preventDefault();
       var nmb = $('#number').val();
       console.log(nmb);
       var submit_btn = $('#submit_btn');
       var product_id = submit_btn.data("t_shirt_id");
       var product_name = submit_btn.data("t_shirt_name");
       var product_price = submit_btn.data("t_shirt_price");
       console.log(product_name);
       console.log(product_id);
       console.log(product_price);
       
       data={};
       data.product_id = product_id
       data.nmb = nmb
       var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
       data["csrfmiddlewaretoken"] = csrf_token
       var url = form.attr("action")
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log("OK");
                 console.log(data.products_total_nmb)
                 if(data.products_total_nmb) {
                    $('#basket_total_nmb').text('#basket_total_nmb').text("("+data.products_total_nmb+")");
                 }
                 $('.basket-items').append('<a class="dropdown-item">' + product_name + ', '+ nmb +' шт. ' + ' по ' + product_price + 'руб.'+
                    '<button type="button" class="close delete-item" aria-label="Close">'+
                    '<span aria-hidden="true">&times;</span>'+
                    '</button>' +
                    '</a>');
             },
             error: function(){
                 console.log("error")
             }
         });


    });

    $(document).on('click', '.delete-item', function(){
        $(this).closest('a').remove();
    })
});
