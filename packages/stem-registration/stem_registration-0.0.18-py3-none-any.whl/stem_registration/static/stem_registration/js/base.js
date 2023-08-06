(function () {


    $('#id_tax_number').attr('pattern', '[0-9]{10-12}');

    // $(".js-example-matcher-start").select2({
    //     width: '100%'
    // });// Отвечает за селекты с полем поиска
    //
    //
    // $('.language__select').select2({
    //     width: '100%',
    //     escapeMarkup: function (markup) {
    //         return markup;
    //     },
    //     minimumResultsForSearch: -1,
    //     templateResult: function (data) {
    //         let arrTime = data.text.split('|')[1];
    //         if (arrTime) {
    //             markup = `<div><img width="25" src=${data.text.split('|')[1]} alt=""></div>`;
    //             return markup;
    //         }
    //     },
    //     templateSelection: function (data) {
    //         markup = `<div><img width="20" src=${data.text.split('|')[1]} alt=""> </div>`;
    //         return markup;
    //     },
    //
    // });

    // Отвечает за селекты с полем поиска

    $('#id_number').inputmask("phone", {
        onKeyValidation: function () { // Отвечает за маску-валидатор в полях с номером телефона
            {
            }
        }
    });


    $('[type="radio"]').on('change', (e) => {
        setChecked($(e.target));// Функция для поиска радио кнопки которая поменялась
        if ($(e.target).attr('id') == 'id_contractor_type_0') {
            $('.name-legal-wrap').addClass('d-none')
        } else {
            $('.name-legal-wrap').removeClass('d-none');
        }

        if ($(e.target).attr('id') == 'id_contractor_type_0') {
            $('#id_name_legal').val($('#id_first_name').val() + ' ' + $('#id_last_name').val())
        }

        if ($(e.target).attr('id') == 'id_contractor_type_1') {
            $('#id_name_legal').val('')
        }

        if ($(e.target).attr('id') == 'id_contractor_type_2') {
            $('#id_name_legal').val('СПД-ФЛ ' + $('#id_first_name').val() + ' ' + $('#id_last_name').val())
        }

    });

    $('#id_first_name, #id_last_name').on('keyup', function () {
        if ($('#id_contractor_type_2').prop('checked')) {
            $('#id_name_legal').val('СПД-ФЛ ' + $('#id_first_name').val() + ' ' + $('#id_last_name').val())
        }else if ($('#id_contractor_type_0').prop('checked')){
            $('#id_name_legal').val($('#id_first_name').val() + ' ' + $('#id_last_name').val())
        }
    });

    function setChecked(e) {
        let id = e.attr('id');
        // console.log($(e))
        $('.block_company [data-toggle]').addClass('d-none');//Замена полей формы при смене радио кнопки
        $(`.block_company [data-toggle=${id}]`).removeClass('d-none');
    }

    $('[type="radio"]').each((i, el) => {
        if ($(el).attr('checked') === 'checked') {// Инициализация формы по заданной радио кнопки после перезагрузки,
            // нужна при ошибке в регистрации что бы форма сохраняла поля по заданной активной кнопке
            setChecked($(el));
        }

    });


    $('input.file').change(function () {

        document.querySelector(`[for=${$(this).attr('id')}] span`).innerHTML = ' ' + '( ' + this.files[0].name + ' )';
    });
})();

