
const btn = document.querySelector('.btn-getfile')
const submit = document.querySelector('.btn-submit')
const fileinput = document.querySelector(".file-input")
const editor = document.querySelector('.editor')
btn.addEventListener('click', e => {
    const filename = fileinput.value.trim()
    if (!filename) {
        return alert("Please input a file name")
    } else if (filename.slice(filename.length - 3) !== '.py') {
        return alert("invalid file name: must be a .py file")
    }
  axios.get(`/files/${filename}`).then(res => {
      console.log('content: ', res.data.data)
      editor.value = res.data.data
  }).catch(e => console.log(e))
}, false)

submit.addEventListener('click', e => {
    const content = editor.value.trim()
    if (!content) {
        return alert("content cannot be empty.")
    }
    const filename = fileinput.value.trim()
    if (!filename) {
        return alert("Please input a filename for your change.")
    }
    axios.put("/files", {content, filename}).then(res => {
        alert(res.data.message)
    }).catch(err => console.log('err res', err.response))
})