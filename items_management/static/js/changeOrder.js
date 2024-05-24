// Эта функция меняет порядок сортировки на противополжный
// Имя сортировки - то имя, которое необходимо указать во view при получении нужного queryset.
// Пример: смотреть в views.py
function changeOrder(sort_name, value_1, value_2, default_value) {
    let url = ''
    let cur_url = window.location.href;
    let includes_qm = cur_url.includes('?')
    let includes_sort = cur_url.includes(sort_name);

    if (!includes_sort && !includes_qm) {
        url = cur_url + `?${sort_name}=` + default_value;
    } else if (includes_qm && !includes_sort) {
        url = cur_url + `&${sort_name}=` + default_value;
    } else {
        if (cur_url.includes(`${sort_name}=${value_1}`)) {            
            url = cur_url.replace(`${sort_name}=${value_1}`, `${sort_name}=${value_2}`);
        } else if (cur_url.includes(`${sort_name}=${value_2}`)) {
            url = cur_url.replace(`${sort_name}=${value_2}`, `${sort_name}=${value_1}`);
        }                
    }
    window.location.href = url;
}

function clearSorts() {
    let url = '';
    let cur_url = window.location.href;
    index_of_qm = cur_url.indexOf('?')
    if (index_of_qm != -1) {
        url = cur_url.slice(0, index_of_qm)
        window.location.href = url;
    }
}