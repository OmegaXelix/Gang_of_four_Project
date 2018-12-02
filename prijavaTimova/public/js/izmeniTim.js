const qs = (selector, node = document) => node.querySelector(selector);
const qsa = (selector, node = document) => Array.from(node.querySelectorAll(selector));

function jsonifyInputs(parent) {
    return qsa("input", parent).reduce((acc, el) => {
        if (el.type === "file") {
            return acc;
        }
        acc[el.name] = el.value;
        return acc;
    }, {});
}

const queryOptions = location.search
    .slice(1)
    .split("&")
    .map(x => x.split("="))
    .reduce((acc, [key, value]) => (acc[key] = value, acc), {});

const imgThreeMembers = qs("#imgThreeMembers");
const imgFourMembers = qs("#imgFourMembers");
imgThreeMembers.click();

function collectAllData() {
    const team = jsonifyInputs(teamInfo);
    team.team_members = teamMembers.map(jsonifyInputs);
    if (fourthMember.style.display === "none") {
        team.team_members.pop();
    }

    return team;
}

function fillInputs(data) {
    qsa("input").filter(x => x !== DOM.uuid).forEach(x => x.value = "");
    qs("#name").value = data.name;
    qs("#description").value = data.description;
    qs("#photo_url").value = data.photo_url;

    const members = qsa(".memberOfGroup");

    members.forEach((member, i) => {
        Object.keys(data.team_members[i] || {})
            .filter(key => key !== "id" && key !== "team_id")
            .forEach(key => {
                qs(`input[name="${key}"]`, member).value = data.team_members[i][key];
            })

    })
}

function showFormMember(showForth){
    $('#divForm').css('width','100%');
    $('#teamMembersRow').css('display','flex');

    if(showForth){
        $('.memberOfGroup').removeClass('col-md-4');
        $('.memberOfGroup').addClass('col-md-3');
        $('#forthMember').css('display','block');
        $('#imgThreeMembers').removeClass('selected');
        $('#imgFourMembers').addClass('selected');

        $('#forthMember input').attr('required', 'required');
    }
    else{
        $('.memberOfGroup').removeClass('col-md-3');
        $('.memberOfGroup').addClass('col-md-4');
        $('#forthMember').css('display','none');
        $('#imgThreeMembers').addClass('selected');
        $('#imgFourMembers').removeClass('selected');

        $('#forthMember input').removeAttr('required');
    }
}


const teamInfo = qs(".opsteInformacije");
const teamMembers = qsa(".memberOfGroup");
const fourthMember = qs("#forthMember");
qs("#forma").addEventListener("submit", e => {
    e.preventDefault();

    const modalOk = $(".js-modal-ok");
    const modalQuit = $(".js-modal-quit");
    API.putTeam(DOM.uuid.value, collectAllData())
        .then(team => {
            modalOk.show();
            modalQuit.hide();
            qs(".js-modal-body").textContent = i18n("Update successful.");
            $("#modal-update-team").modal();
        })
        .catch(err => {
            modalOk.hide();
            modalQuit.show();
            qs(".js-modal-body").textContent = i18n("Error") + ": " + err.message;
            $("#modal-update-team").modal();
        })

})

const DOM = {
    uuid: qs(".js-uuid"),
    uuidSearch: qs(".js-uuid-search"),
    deleteTeam: qs(".js-delete-team"),
};

const photoUrl = qs(`input[name="photo_url"]`);
const photoHolder = qs(`.js-photo-holder`);

// Hidden
DOM.uuidSearch.addEventListener("click", () => {
    API.getTeam(DOM.uuid.value)
        .then(team => {
            if (team.team_members.length === 4) {
                imgFourMembers.click();
            } else {
                imgThreeMembers.click();
            }
            fillInputs(team);
            photoHolder.innerHTML = "";
            const img = new Image(128, 128);
            img.src = photoUrl.value;
            photoHolder.appendChild(img);
        })
        .catch(err => {
            console.error(err);
            alert("Greska: " + err.message);
        });
});

// Hidden
DOM.deleteTeam.addEventListener("click", () => {
    API.deleteTeam(DOM.uuid.value)
        .then(() => {
            alert("Tim izbrisan")
        })
        .catch(err => {
            console.error(err);
            alert("Greska: " + err.message);
        });
});

if (queryOptions.team_uuid) {
    DOM.uuid.value = queryOptions.team_uuid;
    DOM.uuidSearch.click();
}

function random(min, max, inclusive = false) {
    return Math.floor(Math.random() * (max - min + inclusive)) + min;
}


qs(".js-photo-input").addEventListener("change", e => {
    loadImage(e.target.files[0], canvas => {
        const dataURL = canvas.toDataURL();
        photoUrl.value = dataURL;
        photoHolder.innerHTML = "";
        photoHolder.appendChild(canvas);
    }, {canvas: true, maxWidth: 128, maxHeight: 128})
})