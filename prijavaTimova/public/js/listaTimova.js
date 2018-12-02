const qs = (selector, node = document) => node.querySelector(selector);
const qsa = (selector, node = document) => Array.from(node.querySelectorAll(selector));

function Team(team) {
    const {name, description, photo_url, team_members, team_uuid} = team;
    return `
        <div class="team">
            <div class="row mb-0 mb-lg-5">
                <div class="col col-12 col-lg-8">
                    <img class="d-block p-3 mx-auto float-none float-lg-left" src="${photo_url}">
                    <div class="row px-4 text-center u-text-big">
                        ${name}
                    </div>
                    <div class="row pl-4">
                        <span class="u-text-small">${description}</span>
                    </div>
                    </span>
                </div>


                <div class="col col-12 col-lg-4">
                    <div class="row">
                        <div class="col col-12 col-xl-6 mb-2 mb-xl-0">
                            <a href="izmeniTim.html?team_uuid=${team_uuid}"><button class="btn btn-outline-success btn-block my-3 my-lg-0 team__update">${i18n("Update")}</button></a>
                        </div>
                        <div class="col col-12 col-xl-6">
                            <button data-uuid="${team_uuid}" class="btn btn-outline-danger btn-block team__delete">${i18n("Delete")}</button>
                        </div>
                    </div>
                </div>
            </div>

            
            ${team_members.map(Member).join("")}
        </div>
    `.trim();
}

function Member(member) {
    const {first_name, last_name, id} = member;
    return `
        <div class="member row">
            <div class="col col-12 col-lg-6 text-center text-lg-left my-3 my-lg-0">
                <span>${first_name} ${last_name}</span>
            </div>
            <div class="col col-12 col-lg-6">
                <div class="row">
                    <div class="col col-6 col-lg-6">
                        <a href="izmeniClana.html?id=${id}"><button class="btn btn-outline-success mb-sm-3 btn-block member__update">${i18n("Update")}</button></a>
                    </div>

                    <div class="col col-6 col-lg-6">
                        <button data-id="${id}" class="btn btn-outline-danger btn-block member__delete">${i18n("Delete")}</button>
                    </div>
                </div>
            </div>
        </div>
    `.trim();
}

const DOM = {
    teams: qs(".js-teams"),
};

function renderTeams(parent) {
    parent.innerHTML = "";
    API.getTeams()
    .then(teams => {
        const a = teams.map(Team).join("");
        parent.insertAdjacentHTML("beforeend", a);
        qsa(".member__delete").forEach(deleteButton => {
            deleteButton.addEventListener("click", () => deleteEntry(deleteButton.dataset.id, "member"));
        });

        qsa(".team__delete").forEach(deleteButton => {
            deleteButton.addEventListener("click", () => deleteEntry(deleteButton.dataset.uuid, "team"));
        });
    });
}

function deleteEntry(id, teamOrMember) {
    const fn = teamOrMember === "team" ? API.deleteTeam : API.deleteMember;

    fn(id)
        .then(() => {
            qs(".js-modal-body").textContent = i18n("Delete successful.");
            $("#modal-delete-team").modal();
            renderTeams(DOM.teams);
        })
        .catch(err => {
            console.log(err);
            qs(".js-modal-body").textContent = i18n("Error") + ": " + err.message;
            $("#modal-delete-team").modal();
            renderTeams(DOM.teams);
        });
}

renderTeams(DOM.teams);
