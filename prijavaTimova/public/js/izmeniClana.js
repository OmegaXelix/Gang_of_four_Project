const qs = (selector, node = document) => node.querySelector(selector);
const qsa = (selector, node = document) => Array.from(node.querySelectorAll(selector));

function jsonifyInputs(parent) {
    return qsa("input", parent).reduce((acc, el) => {
        acc[el.name] = el.value;
        return acc;
    }, {});
}

const queryOptions = location.search
    .slice(1)
    .split("&")
    .map(x => x.split("="))
    .reduce((acc, [key, value]) => (acc[key] = value, acc), {});

function collectAllData() {
    const member = jsonifyInputs(qs(".memberOfGroup"));
    return member;
}

function fillInputs(data) {
    const member = qs(".memberOfGroup");
    Object.keys(data || {})
        .filter(key => key !== "id" && key !== "team_id")
        .forEach(key => {
            qs(`input[name="${key}"]`, member).value = data[key];
        });
}


const teamMembers = qsa(".memberOfGroup");

const DOM = {
    id: qs(".js-member-id"),
    idSearch: qs(".js-member-id-search"),
    updateMember: qs(".js-update-member"),
    deleteMember: qs(".js-delete-member"),
};

// Hidden
DOM.idSearch.addEventListener("click", () => {
    API.getMember(DOM.id.value)
        .then(member => {
            fillInputs(member);
        })
        .catch(err => {
            console.error(err);
            alert("Greska: " + err.message);
        });
})

qs("#forma").addEventListener("submit", e => {
    e.preventDefault();
    const data = collectAllData();

    const modalOk = $(".js-modal-ok");
    const modalQuit = $(".js-modal-quit");
    API.putMember(DOM.id.value, data)
        .then(member => {
            modalOk.show();
            modalQuit.hide();
            qs(".js-modal-body").textContent = i18n("Update successful.");
            $("#modal-update-team").modal();
        })
        .catch(err => {
            modalOk.hide();
            modalQuit.show();
            console.error(err);
            qs(".js-modal-body").textContent = i18n("Error") + ": " + err.message;
            $("#modal-update-team").modal();
        });
});

DOM.deleteMember.addEventListener("click", () => {
    API.deleteMember(DOM.id.value)
        .then(() => {
            qs(".js-modal-body").textContent = i18n("Delete successful.");
            $("#modal-update-team").modal();
        })
        .catch(err => {
            console.error(err);
            qs(".js-modal-body").textContent = i18n("Error") + ": " + err.message;
            $("#modal-update-team").modal();
        });
});

if (queryOptions.id) {
    DOM.id.value = queryOptions.id;
    DOM.idSearch.click();
}