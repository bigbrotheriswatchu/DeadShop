$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    function basketUpdating(product_id, nmb, is_delete){
       var data={};
       data.product_id = product_id
       data.nmb = nmb
         var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
         data["csrfmiddlewaretoken"] = csrf_token;

       if (is_delete){
            data["is_delete"] = true;
       }

       var url = form.attr("action")
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log("OK");
                 console.log(data.products_total_nmb)
                 if(data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                    console.log(data.products);

                    $('.basket-items').html("");
                    $.each(data.products, function(key, value){
                        $('.basket-items').append(
                            '<a class="dropdown-item">'+value.name+', '+value.nmb+' шт.'+value.price_per_item+' руб'+
                            '<p class="delete-item d-inline" data-product_id="'+value.id+'"> X</p>'+
                            '</a>'
                        );
                    })
                 }
             },
             error: function(){
                 console.log("error")
             }
         });
    }


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

       basketUpdating(product_id, nmb, is_delete=false)

    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true)
    });


    function calculatingBasketAmount(){
        console.log("calculatingBasketAmount");
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function() {
            console.log($(this).text());
            total_order_amount += parseInt($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount);

    };
    console.log("123");
    calculatingBasketAmount();
});
