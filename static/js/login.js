document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    if (!usernameInput || !passwordInput) {
        alert("Form öğeleri bulunamadı.");
        return;
    }

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
        alert("Lütfen tüm alanları doldurun.");
        return;
    }

    fetch("/auth/token", {
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
                localStorage.setItem("token", data.access_token);
                window.location.href = "/home"; // Giriş başarılıysa anasayfaya yönlendir
            }
        })
        .catch(error => {
            alert("Hatalı kullanıcı adı veya şifre.");
            console.error(error);
        });
});

