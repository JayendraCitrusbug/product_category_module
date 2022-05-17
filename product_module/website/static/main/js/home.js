// window.onload = initAll;

// var cat;

// function initAll(){
// }

$(document).ready(function () {
    // $(".nothing").addClass("d-none");
    // let arr = [];
    // $('.j').each(function (i, obj) {
    //     cat = obj.innerText;
    //     arr.push(cat);
    // });

    $('.j').on('click', function () {
        var c = $(this).text().replace(/\s/g, '');
        // console.log(c)
        var l = $('.filterproductrow');

        for (var i = 0; i < l.length; i++) {
            let str = "";
            str = l[i].innerText;
            var nospace = str.replace(/\s/g, '');

            if (nospace.match(c)) {
                $(".filterproductrow").eq(i).removeClass("d-none").index(i);
                // $(".nothing").removeClass("d-none");
            } else {
                $(".filterproductrow").eq(i).addClass("d-none").index(i);
                // $(".nothing").addClass("d-none");
            }
        }
    });


    $('#button').on('click', function () {
        let searched = $('#search').val();
        $.ajax({
            type: "get",
            url: "/search/",
            data: { search: searched },
            success: function (data) {
                let a = JSON.parse(data)
                console.log('SUCCESS');
                console.log(data);
                $('.main').empty()

                for (const key in a) {
                    let b = a[key].fields;
                    $('.main').append(`
                    <div class="card h-90 text-center shadow p-3 bg-body rounded">
                        <div class="text-center mt-1">
                            <img src="/media/${b.img}" class="img-fluid rounded-start" alt="product_image">
                        </div>
                            <div class="card-body text-center">
                            <h5 class="card-title">Name :- ${b.product_name}</h5>
                            <p class="card-text">Description :- ${b.description}</p>
                            <h5 class="card-text"><b>Price : ₹</b>${b.price}</h5>
                        </div>
                        <div class="card-footer">
                            <small class="text-muted"><a href="/readmore/${a[key].pk}/" class="btn btn-primary">Buy
                                Now</a></small>
                            <small class="text-muted"><a href="/readmore/${a[key].pk}/" class="btn btn-secondary">Read
                                More</a></small>
                        </div>
                    </div>
                    `)
                }
            },

            failure: function () {
                console.log('FAIL');
                console.log(data);
            }
        });
    });

});