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

qs("#imgThreeMembers").click();

function collectAllData() {
    const team = jsonifyInputs(teamInfo);
    team.team_members = teamMembers.map(jsonifyInputs);
    if (fourthMember.style.display === "none") {
        team.team_members.pop();
    }

    return team;
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
    API.postTeam(collectAllData())
        .then(team => {
            modalOk.show();
            modalQuit.hide();
            qs(".js-modal-body").textContent = i18n("Create successful.");
            $("#modal-create-team").modal();
        })
        .catch(err => {
            modalOk.hide();
            modalQuit.show();
            console.error(err);
            qs(".js-modal-body").textContent = i18n("Error") + ": " + err.message;
            $("#modal-create-team").modal();
        });
})

function random(min, max, inclusive = false) {
    return Math.floor(Math.random() * (max - min + inclusive)) + min;
}

const photoUrl = qs(`input[name="photo_url"]`);
const photoHolder = qs(`.js-photo-holder`);
photoUrl.value = "/img/planet-" + random(1, 7, true) + ".png";
photoHolder.innerHTML = "";
const img = new Image(128, 128);
img.src = photoUrl.value;
photoHolder.appendChild(img);


qs(".js-photo-input").addEventListener("change", e => {
    loadImage(e.target.files[0], canvas => {
        const dataURL = canvas.toDataURL();
       photoUrl.value = dataURL;
        photoHolder.innerHTML = "";
        photoHolder.appendChild(canvas);
    }, {canvas: true, maxWidth: 128, maxHeight: 128})
})