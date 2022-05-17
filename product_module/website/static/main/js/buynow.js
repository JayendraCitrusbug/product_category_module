$(document).ready(function(){
    $("#plus").click(function(event){
        event.preventDefault()
        let pid = $(this).attr('pid')
        let max = $(this).attr('val')
        let x = $("#quantity").val()
        let z = parseInt(x);

        if(z<max)
            quantity = z+1
            
        $("#quantity").val(quantity)
        price=$("#price").val()
        total_price=price*quantity
        $("#total_price").val(total_price);
    });
});


$(document).ready(function(){
    $("#minus").click(function(event){
        event.preventDefault()
        let pid = $(this).attr('pid')
        let x = $("#quantity").val()
        let z = parseInt(x);

        if(z>1){
            quantity = z-1
        }else{
            quantity=1
        }

        $("#quantity").val(quantity)
        price=$("#price").val()
        total_price=price*quantity
        $("#total_price").val(total_price);
    });
});


// $(document).ready(function(){
//     $("#buynow").click(function(){
//         quantity = $("#quantity").text()
//         total_price = $("#total_price").val();
//         id = $("#id").val()
//         var csrf = document.querySelector("input[name='csrfmiddlewaretoken']").value;
//         $.ajax({
//             url : `/buynow/${id}/`,
//             method : "POST",
//             data : {'quantity':quantity, 'total_price':total_price, 'csrfmiddlewaretoken':csrf},
//         })
//     })
// })
