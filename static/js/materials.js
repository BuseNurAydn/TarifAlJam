async function malzemeEkle() {
  const input = document.getElementById("malzemeInput");
  const malzemeAdi = input.value.trim();

  if (malzemeAdi === "") return;

  const materialData = {
    material_name: malzemeAdi,
    isExpiring: false,
    ExpirationDate: null
  };

  console.log("POST edilecek veri:", materialData);

  try {
    const response = await fetch("/materials/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(materialData)
    });

    if (!response.ok) {
      const err = await response.text();
      throw new Error(`Hata: ${response.status} - ${err}`);
    }

    const savedMaterial = await response.json();
    console.log("Kaydedilen malzeme:", savedMaterial);

    const liste = document.getElementById("malzemeListesi");

    const malzemeDiv = document.createElement("div");
    malzemeDiv.className = "malzeme-item";
    malzemeDiv.innerHTML = `
      <span>${savedMaterial.material_name}</span>
      <label>
        <input type="checkbox" /> Bozulmak Üzere
      </label>
      <button onclick="this.parentElement.remove()">Sil</button>
    `;
    liste.appendChild(malzemeDiv);
    input.value = "";
  } catch (error) {
    console.error("Malzeme eklenemedi:", error);
    alert("Malzeme eklenirken hata oluştu. Detay için konsolu kontrol et.");
  }
}
