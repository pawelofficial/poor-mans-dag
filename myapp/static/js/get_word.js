fetch('/keyword', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ keyword: 'example' }),
})
.then(response => response.json())
.then(data => console.log(data));