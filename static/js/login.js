document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Lütfen tüm alanları doldurun.");
        return;
    }

    fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            username: username,
            password: password,
        }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Giriş başarısız");
            }
            return response.json();
        })
        .then(data => {
            if (data.access_token) {
                // Token'ı localStorage ya da cookie'de saklayabilirsin
                localStorage.setItem("token", data.access_token);

                //  Giriş başarılıysa yönlendirme yap
                window.location.href = "/";
            }
        })
        .catch(error => {
            alert("Hatalı kullanıcı adı veya şifre.");
            console.error(error);
        });
});
