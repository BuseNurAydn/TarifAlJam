// Malzeme ekleme , silme
function malzemeEkle() {
    const input = document.getElementById("malzemeInput");
    const malzemeAdi = input.value.trim();
  
    if (malzemeAdi === "") return;
  
    const liste = document.getElementById("malzemeListesi");
  
    const malzemeDiv = document.createElement("div");
    malzemeDiv.className = "malzeme-item";
  
    malzemeDiv.innerHTML = `
      <span>${malzemeAdi}</span>
      <label>
        <input type="checkbox" /> Bozulmak Üzere
      </label>
      <button onclick="this.parentElement.remove()">Sil</button>
    `;
  
    liste.appendChild(malzemeDiv);
    input.value = "";
  }
  
  function tarifOner() {
    alert("Tarif önerileri hazırlanıyor...");
  }
  