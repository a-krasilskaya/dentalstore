$( document ).ready(function() {
    $(function() {
     let header = $('.header');
     let hederHeight = header.height();

         $(window).scroll(function() {
           if($(this).scrollTop() > 1) {
            header.addClass('sticky-top');
            $('body').css({
               'paddingTop': hederHeight+'px' // делаем отступ у body, равный высоте шапки
            });
           } else {
            header.removeClass('sticky-top');
            $('body').css({
             'paddingTop': 0 // удаляем отступ у body, равный высоте шапки
            })
           }
         });
    });

   // Подсветка меню
   $(function(){
        let loc = window.location.pathname;
        $('.nav-link').each(function(){
            $(this).toggleClass('active', $(this).attr('href') == loc);
        });
    });

    $('.owl-carousel').owlCarousel({
    items:4,
    loop:true,
    margin:20,
    dots:false,
    nav:true,
//    autoplay:true,
    autoplaySpeed:3000,
    navSpeed:1000,
    drugEndSpeed:1000,
    navText: [
          '<svg fill="#4b5196" width="35" height="35" viewBox="0 0 24 24"><path d="M16.67 0l2.83 2.829-9.339 9.175 9.339 9.167-2.83 2.829-12.17-11.996z"/></svg>',
          '<svg fill="#4b5196" width="35" height="35" viewBox="0 0 24 24"><path d="M5 3l3.057-3 11.943 12-11.943 12-3.057-3 9-9z"/></svg>'
            ],
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        }
    });


    $('.helptext').click(function(){ // задаем функцию при нажатиии на элемент <button>
        if ($('input[type=checkbox]').is(':checked')){
            $('input[type=checkbox]').prop('checked', false);
        } else {
            $('input[type=checkbox]').prop('checked', true);
        }
    });

    $('.small a').click(function(e){
        $('.small a').removeClass('active');
        if($('.big img').attr('src')!==$(this).attr("href")){
            $('.big img').hide().attr('src', $(this).attr("href")).fadeIn(1000);
            $(this).addClass('active');
        }
        e.preventDefault();
    });


    $('.feedback-form').submit(function(e) {
        e.preventDefault()
        $.ajax({
            url: this.action,
            type: this.method,
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){
                $('.alert').addClass('alert-success').removeClass('d-none')
                $('.alert-success .reviews').text('Спасибо за заявку, наш сотрудник позвонит вам в ближайшее время')
                $(".feedback-form").trigger("reset");
            },
            error: function(response) {
                console.log('err', response)
                if (response.status === 400){
                    $('.alert').addClass('alert-danger').removeClass('d-none')
                    $('.alert-danger .reviews').text('Заполните обязательные поля')
                }
            },
        })
    });


    $('.add-to-cart form label').text('Количество:')


// фильтры
//    $('.sidebar .form_filter_checkbox label').click(function(){
//        if ($('input[type=checkbox]').is(':checked')){
//            $('input[type=checkbox]').prop('checked', false);
//            $(this).toggleClass('checked-item')
//        } else {
//            $('input[type=checkbox]').prop('checked', true);
//        }
//    });

// скрыть показать фильтры на мобильных
    $('.mobile-filter-btn').click(function(){
        $('.wrap-mobile-filter').toggleClass('d-none').fadeIn(500);
//        if ($('.wrap-mobile-filter').hasClass('d-none')){
//            $('.mobile-filter-btn img').attr({'src': "{% static '/catalog/images/filter.png' %}",
//            'alt': 'filter'});
//        } else {
//            $('.mobile-filter-btn img').attr({'src': "{% static '/catalog/images/close.png' %}",
//            'alt': 'close'});
//        }
    });


//    cart
    $('.add-cart').click(function(){
        if ($(this).hasClass('list-products')){
            $(this).hide();
        }else{
            $(this).text('Добавить еще');
        }
        $(this).siblings('.in-cart').removeClass('d-none').addClass('d-flex');
    });

    $('.in-cart .btn').click(function(e){
        e.preventDefault()
        window.location.href = '/cart/';
    });


    $(".add-to-cart-ajax").submit(function(e) {
        e.preventDefault()
        $.ajax({
            url: this.action,
            type: this.method,
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
                let cartCount = +($('.count-cart').text()) + Number($('#id_quantity').val())
                $('.count-cart').text(cartCount)
            },
            error: function(response) {
                console.log('err', response)
            },
        })
    });


// Подгрузка товаров ajax
    // Переменная для хранения текущей страницы
//    let currentPage = 1;
//
//    // Функция для отправки Ajax-запроса на сервер
//    function loadMoreProducts() {
//      // Создание и настройка объекта XMLHttpRequest
//      const xhr = new XMLHttpRequest();
//      xhr.open('GET', `/products?page=${currentPage}`, true);
//
//      // Обработка успешного ответа от сервера
//      xhr.onload = function() {
//        if (xhr.status >= 200 && xhr.status < 400) {
//          const response = JSON.parse(xhr.responseText);
//          const products = response.products;
//
//          // Обновление страницы с новыми товарами
//          const productList = document.getElementById('productList');
//          products.forEach(product => {
//            const productElement = document.createElement('div');
//            productElement.textContent = product.name;
//            productList.appendChild(productElement);
//          });
//
//          // Увеличение номера текущей страницы
//          currentPage++;
//
//          // Если больше нет товаров, скрываем кнопку или блок для подгрузки
//          if (!response.has_next) {
//            const loadMoreButton = document.getElementById('loadMoreButton');
//            loadMoreButton.style.display = 'none';
//          }
//        }
//      };
//
//      // Отправка запроса на сервер
//      xhr.send();
//    }
//
//    // Функция для обработки события скролла страницы
//    function handleScroll() {
//      // Если достигнут конец страницы, вызываем функцию для загрузки новых товаров
//      if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
//        loadMoreProducts();
//      }
//    }

    // Добавляем обработчик события скролла страницы
//    window.addEventListener('scroll', handleScroll);

//    $.ajax({
//        url: '/products/paginations',
//        method: 'GET',
//        data: { category: 'anesteziya' }, // Замените 'your_category_slug' на актуальное значение
//        success: function(response) {
//
//            // Обработка успешного ответа от сервера
//            console.log(response); // Выводим ответ в консоль
//        },
//        error: function(xhr, status, error) {
//            // Обработка ошибки запроса
//            console.error(error); // Выводим ошибку в консоль
//        }
//    });

});




