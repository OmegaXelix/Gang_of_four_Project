(function main() {
    const db = {
        "sr": {
            "Notification": "Obaveštenje",
            "Update": "Ažuriraj",
            "Delete": "Obriši",

            // Modal content
            "Create successful.": "Kreiranje uspešno.",
            "Delete successful.": "Brisanje uspešno.",
            "Update successful.": "Ažuriranje uspešno.",

            "Error": "Greška",
            "Name": "Ime",
            "Description": "Opis",
            "Photo URL": "URL slike",
            "First name": "Ime",
            "Last name": "Prezime",
            "Email": "Email",
            "City": "Grad",
            "Phone number": "Broj telefona",
            "School": "Škola",
            "Team information": "Informacije o timu",

            "First member": "Prvi član",
            "Second member": "Drugi član",
            "Third member": "Treći član",
            "Fourth member": "Četvrti član",

            "Create team": "Kreiraj tim",
            "Update team": "Ažuriraj tim",
            "Update member": "Ažuriraj člana",
            "Team list": "Lista timova",

            "Back": "Nazad",
            "English": "Engleski",
            "Serbian": "Srpski",

            "Secret": "Tajna",
            "Secret 90s web design mode": "Tajni veb dizajn mod iz devedesetih",
            "is activated": "je uključen",
            "is deactivated": "je isključen",

            "Activate": "Uključi",
            "Deactivate": "Isključi",
        }
    }

    function changeLanguage(lang) {
        const old = localStorage.getItem("language") || "sr";
        if (lang === old) {
            return;
        }
        localStorage.setItem("language", lang);
        location.reload();
    }

    document.body.innerHTML = document.body.innerHTML.replace(/{{([\w ]+)}}/g, (_, word) => i18n(word));
    document.title = i18n(document.title) || document.title;

    function appendButtons(parent) {
        const lang = localStorage.getItem("language") || "sr";
        const english = document.createElement("button");
        english.classList.add("btn", "btn-outline-light", "btn-block");
        english.classList.toggle("active", lang === "en");
        english.textContent = i18n("English");
        english.addEventListener("click", () => changeLanguage("en"));
        parent.appendChild(english);
        
        const serbian = document.createElement("button");
        serbian.classList.add("btn", "btn-outline-light", "btn-block", "mb-4", "mb-lg-0");
        serbian.classList.toggle("active", lang === "sr");
        serbian.textContent = i18n("Serbian");
        serbian.addEventListener("click", () => changeLanguage("sr"));
        parent.appendChild(serbian);
    }

    const i18nButtonParent = document.querySelector(`[data-i18n]`);
    if (i18nButtonParent) {
        appendButtons(i18nButtonParent);
    }

    function i18n(str) {
        const lang = localStorage.getItem("language") || "sr";
        return lang === "en" ? str : db.sr[str];
    }

    i18n.appendButtons = appendButtons;

    window.i18n = i18n;
})();