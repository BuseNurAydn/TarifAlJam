document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const username = document.getElementById("username").value.trim();
    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const role = document.getElementById("role").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (
      !email || !username || !firstName || !lastName ||
      !role || !phone || !password || !confirmPassword
    ) {
      alert("Lütfen tüm alanları doldurun.");
      return;
    }

    if (password !== confirmPassword) {
      alert("Şifreler eşleşmiyor!");
      return;
    }

    alert("Kayıt başarılı! (örnek)");

  });
