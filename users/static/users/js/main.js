const countEl = document.getElementsById('count');

updateVisitorCount()

function updateVisitorCount(){
    fetch('https://api.countapi.xyz/update/smart-fit/youtube/?amount=1')
    .then(res => res.json())
    .then(res => {
        countEl.innerHTML = res.value;
    })
}