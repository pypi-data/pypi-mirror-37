/**
 * Created by bee on 2018/9/26.
 */
function add_question(questions_vm,post_url,section_id, type_id) {
    var params = new FormData();
    params.append("section_id", section_id);
    params.append("type_id", type_id);
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.post(post_url, params).then(function (resp) {
        if (resp.data.error == 0) {
            questions_vm.questions.push(JSON.parse(resp.data.new_question))
        }

    });
}