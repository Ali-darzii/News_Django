function DeleteAccount() {
    let box = 'not_checked';
    if ($('#deleteaccountCheck').is(":checked")) {
        box = 'checked';
    }
    $.ajax({
        url: '/user/remove-account/',
        datatype: 'json',
        method: 'POST',
        data: {
            box: box
        },
        beforeSend: function (xhr) {
            const csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (res) {
            if (res.status === 'error') {
                $('#remove-account-ajax').html(res.data)
            } else {
                setTimeout(function () {
                    console.log('qwer');
                }, 5000);
                window.location.assign('http://127.0.0.1:8000/');
            }
        },
    });
}

/*article like or dislike*/
function articleLike(articleId) {
    const _likeBtn = document.getElementById('heart-like');
    $.ajax({
        url: '/articles/like/process/',
        data: {
            article_id: articleId,
        },
        datatype: 'json',
        method: 'GET',
        beforeSend: function () {

        },
        success: function (res) {
            if (res.status === 'like') {
                _likeBtn.classList.add('text-danger');
                $('#total-like').html(res.data);
            } else {
                _likeBtn.classList.remove('text-danger');
                $('#total-like').html(res.data);
            }

        }
    });

}

/*load more Article in every category*/
function loadMoreTechArticle(cat) {
    const load_btn = document.getElementById('load-btn');
    const spinner = document.getElementById('spinner');
    const alert = document.getElementById('alert');
    var _currentItem = $('.article_number').length;
    $.ajax({
        url: '/articles/load-more/',
        data: {
            lengths: _currentItem,
            category: cat
        },
        datatype: 'json',
        method: 'GET',
        beforeSend: function () {
            load_btn.classList.add('like-btn');
            spinner.classList.remove('like-btn');

        },
        success: function (res) {
            if (res.status === 'success') {
                spinner.classList.add('like-btn');
                load_btn.classList.remove('like-btn');
                $('#tech-ajax').append(res.data);
            } else {
                spinner.classList.add('like-btn');
                load_btn.classList.add('like-btn');
                alert.classList.remove('like-btn');
            }

        }
    });
}

/*delete avatar in user_panel */
function deleteAvatar() {
    $.ajax({
        url: '/user/remove-user-avatar/',
        datatype: 'json',
        method: 'POST',
        beforeSend: function (xhr) {
            const csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (res) {
            if (res.status === 'success') {
                $("#head_avatar").html(res.head_avatar);
                $("#profileDropdown").html(res.header_avatar_1);
                $("#header_avatar_2").html(res.header_avatar_2);
                $("#form_avatar").html(res.form_avatar);
            }
        },
    });
}


/*remove product order in header*/
function removeOrderDetail(_detailId) {
    $.ajax({
        url: '/order-basket/remove-product-order/',
        data: {
            detail_id: _detailId,
        },
        datatype: 'json',
        beforeSend: function () {
        },
        success: function (res) {
            if (res.status === 'success') {
                $("#offcanvasMenu").html(res.orderBasket);
                $("#count_header").html(res.orderCount);
            } else if (res.status === 'not_found_detail_id') {

            } else if (res.status === 'detail_not_found') {

            }
        },
    });
}

/*product count changing in head */
function changeOrderDetailCount(_detailId, _state) {
    $.ajax({
        url: '/order-basket/change-product-order-count/',
        data: {
            detail_id: _detailId,
            state: _state
        },
        datatype: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            if (res.status === 'success') {
                $("#offcanvasMenu").html(res.orderBasket);
                $("#count_header").html(res.orderCount);
            } else if (re.status === 'Detail_not_found') {

            } else if (res.status === 'not_found_detail_or_status') {

            } else if (res.status === 'state_invalid') {

            }
        },
    });
}

/*remove product order in basket_page*/
function removeOrderDetailInBasketPage(_detailId) {
    $.ajax({
        url: '/order-basket/remove-product-order/basket-page/',
        data: {
            detail_id: _detailId,
        },
        datatype: 'json',
        beforeSend: function () {
        },
        success: function (res) {
            if (res.status === 'success') {
                $("#order-basket-page").html(res.data);
            } else if (res.status === 'not_found_detail_id') {

            } else if (res.status === 'detail_not_found') {

            }
        },
    });
}

/*product count changing in basket_page*/
function changeOrderDetailCountInBasketPage(_detailId, _state) {
    $.ajax({
        url: '/order-basket/change-product-order-count/basket-page/',
        data: {
            detail_id: _detailId,
            state: _state
        },
        datatype: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            if (res.status === 'success') {
                $("#order-basket-page").html(res.data);
            } else if (re.status === 'Detail_not_found') {

            } else if (res.status === 'not_found_detail_or_status') {

            } else if (res.status === 'state_invalid') {

            }
        },
    });
}

/*add product to order in product list and product detail*/
function add_product_to_order(_productId, _origin) {
    let _count = '1'
    if (_origin === 'true') {
        _count = $('#product-count').find(":selected").val();
    }
    $.ajax({
        url: '/order-basket/add-product-to-order/',
        data: {
            product_id: _productId,
            count: _count
        },
        datatype: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            if (res.status === 'success') {
                $("#offcanvasMenu").html(res.orderBasket);
                $("#count_header").html(res.orderCount);
                Swal.fire({
                    position: 'top-start',
                    icon: 'success',
                    title: 'کالا مورد نظر داخل سبد کالا قرار گرفت',
                    showConfirmButton: false,
                    timer: 1500
                })

            } else if (res.status === 'not_auth') {
                Swal.fire({
                    title: '<strong>کالا وارد سبد کالا نشد!</strong>',
                    icon: 'error',
                    html:
                        'شما باید وارد ' +
                        '<a href="http://127.0.0.1:8000/sign-in">حساب کاربری</a> ' +
                        'خود بشوید',
                })
            } else if (res.status === 'product_not_found') {

            } else if (res.status === 'invalid_count') {

            }

        }
    });
}

/*like diss like in product detail comment*/
function likeComment(_commentId, _deside) {
    const _Product = document.getElementById("Products").value;
    $.ajax({
        url: '/products/comment/like-dislike/',
        data: {
            comment_id: _commentId,
            deside: _deside,
            product_id: _Product
        },
        datatype: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            $("#like-dislike-ajax").html(res.data);
        }
    });
}

/*choosing star in product detail comment section*/
function starChanger(_Star) {
    $("#starHolder").val(_Star);
}

/*comment submit in product detail */
function commentSubmit() {
    const _Star = document.getElementById("starHolder").value;
    const _Text = document.getElementById("TextAreaComment").value;
    const _Product = document.getElementById("Products").value;

    $.ajax({
        url: '/products/comment/',
        data: {
            star: _Star,
            text: _Text,
            Products_id: _Product
        },
        datatype: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            if (res.status === 'success') {
                $("#rateAndreview").html(res.data);
                $("#low_char").hide();

            } else if (res.status === 'low_char') {
                $("#low_char").show();
            }
        }
    });

}

/*select image in user_panel*/
function selectedImage(_imageUrl) {
    document.getElementById('Big_image').src = _imageUrl;

}

/*Choosing to sort with search or filter*/
function sortedProduct(sortValue) {
    let _Deside = document.getElementById("Deside").value;

    if (_Deside === 'search') {
        searchProduct();
    } else {
        filterProduct();
    }

}

/*choosing pagination for search or filter */
function fillPage(page) {
    $('#page').val(page);
    let _Deside = document.getElementById("Deside").value;
    if (_Deside === 'search') {
        searchProduct();
    } else {
        filterProduct();
    }
}

/*filter product in product list*/
function filterProduct() {
    let _sortSelect = $("#sortSelect").val();
    $("#Deside").val("checkBox");
    let _page = document.getElementById("page").value;
    let _filterObj = {};
    $(".form-check-input").each(function (index, ele) {
        let _filterVal = $(this).val();
        let _filterKey = $(this).data('filter');
        _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function (el) {
            return el.value;
        });

    });
    const spinner = document.getElementById('spinner');
    const pagination = document.getElementById('page_ul');
    $.ajax({
        url: '/products/filterProduct/?page=' + _page + '&' + 'sort=' + _sortSelect,
        data: _filterObj,
        datatype: 'json',
        beforeSend: function () {
            $(".product-box").each(function (index, item) {
                this.parentNode.removeChild(this);
            });
            pagination.parentNode.removeChild(pagination);
            spinner.classList.remove('like-btn');

        },
        success: function (res) {
            // spinner.classList.add('like-btn');
            if (res.status === 'success') {
                $("#filteredProducts").html(res.data);
            }
        }
    });

}

/*search in product list*/
function searchProduct() {
    let _sortSelect = $("#sortSelect").val();
    $("#Deside").val("search");
    let _page = document.getElementById("page").value;
    let _search = $("#q").val();
    const spinner = document.getElementById('spinner');
    const allProduct = document.getElementById('GooGooli');
    $.ajax({
        url: '/products/search/?page=' + _page,
        type: 'GET',
        data: {
            q: _search,
            sort: _sortSelect,
        },
        datatype: 'json',
        beforeSend: function () {
            allProduct.classList.add('like-btn');
            spinner.classList.remove('like-btn');

        },

        success: function (res) {
            if (res.status === 'success') {
                spinner.classList.add('like-btn');
                allProduct.classList.remove('like-btn');
                $("#filteredProducts").html(res.data);
            }
            if (res.status === 'not_found') {
                // $("#filteredProducts").html()
                Swal.fire({
                    icon: 'error',
                    title: 'محصولی یافت نشد!!',
                })
            }
            if (res.status === 'empty') {
                filterProduct();
            }
        }
    });
}


$(document).ready(function () {
    $("#low_char").hide();
    $("#ajaxLoader").hide();
    /*un/show password in user panel*/
    $('#togglelink').unbind().click(function (e) {
        e.preventDefault();
        var password = $('#pass_show');
        var pass_type = password.attr('type');
        if (pass_type === 'password') {
            password.attr('type', 'text');

        } else {
            password.attr('type', 'password');
        }
    });

    /*selecting image for user profile*/
    $("#uploadButton").on("click", function (e) {
        e.preventDefault();
        $("#imageInput").click();
    });
    $("#imageInput").on("change", function () {

        let file = $('#imageInput')[0].files[0];

        $("#imagePreview").html(`<img src="${URL.createObjectURL(file)}" alt="Uploaded Image">`);
        $("#imageName").text(`عکس انتخاب شده: ${file.name}`);
        $("#deleteButton").show();
        var formData = new FormData();
        formData.append('image', file);

    });
    /* un/show delete button of avatar*/
    $("#deleteButton").on("click", function (e) {
        e.preventDefault();
        $("#imagePreview").empty();
        $("#imageName").empty();
        $("#deleteButton").hide();
        $("#imageInput").val(""); // Clear the file input
    });
    /*in search box enter action*/
    $("#q").on('keyup', function (e) {
        if (e.key === 'Enter' || e.keyCode === 13) {
            searchProduct();
        }
    });

});
/*first form of user_panel*/
let origin_form = document.getElementById("origin_form");
origin_form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(origin_form);

    $.ajax({
        url: '/user/user-account-edit/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        datatype: 'json',
        beforeSend: function (xhr) {
            const csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (res) {
            if (res.status === 'success') {
                $("#origin_ajax").html(res.form_data);
                $("#head_avatar").html(res.head_avatar);
                $("#profileDropdown").html(res.header_avatar_1);
                $("#header_avatar_2").html(res.header_avatar_2);
                $("#top-info").html(res.top_info);
                Swal.fire({
                    position: 'top-start',
                    icon: 'success',
                    title: 'حساب کاربری شما بروزرسانی شد',
                    showConfirmButton: false,
                    timer: 1500
                })

            }
        },
    });

});
/*second form of user_panel*/
let profile_form = document.getElementById('profile-form');
profile_form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(profile_form);
    $.ajax({
        url: '/user/profile-user-edit/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        datatype: 'json',
        beforeSend: function (xhr) {
            const csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (res) {
            if (res.status === 'success') {
                $("#profile_ajax").html(res.profile_form);
                Swal.fire({
                    position: 'top-start',
                    icon: 'success',
                    title: 'پروفایل شما بروزرسانی شد',
                    showConfirmButton: false,
                    timer: 1500
                })
            }
        },
    });

});

/*password form of user_panel*/
let password_form = document.getElementById('password-form');
password_form.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(password_form);
    $.ajax({
        url: '/user/change-password-user-panel/',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        datatype: 'json',
        beforeSend: function (xhr) {
            const csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function (res) {
            if (res.status === 'success') {
                window.location.assign('http://127.0.0.1:8000/sign-in');
            } else {
                $("#password-ajax").html(res.password_form);
            }
        },
    });
});






