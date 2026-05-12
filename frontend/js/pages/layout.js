function paginaLayout() {
    return `
        <aside>
            <h2>Menu</h2>
            <ul>
                <li><button id="btn-dashboard" onclick="renderizarSection('dashboard', event)">Dashboard</button></li>
                <li><button id="btn-receitas" onclick="renderizarSection('receitas', event)">Cadastro de Receitas</button></li>
                <li><button id="btn-despesas" onclick="renderizarSection('despesas', event)">Cadastro de Despesas</button></li>
                <li><button id="btn-relatorio" onclick="renderizarSection('relatorio', event)">Relatorio</button></li>
                <li><button id="btn-sair" onclick="renderizarSection('sair', event)">Sair</button></li>
            </ul>
        </aside>

        <main id="section">
        </main>
    `;
}

function setupLayout() {
    renderizarSection('dashboard');
}

function renderizarSection(pagina, evento) {
    const section = document.getElementById('section');

    // Remove a classe 'active' de todos os botões
    document.querySelectorAll('aside button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Adiciona a classe 'active' no botão clicado ou no correspondente
    if (evento) {
        evento.target.classList.add('active');
    } else {
        document.getElementById(`btn-${pagina}`).classList.add('active');
    }

    switch (pagina) {
        case 'dashboard':
            section.innerHTML = paginaDashboard();
            break;
        case 'receitas':
            section.innerHTML = paginaReceitas();
            break;
        case 'despesas':
            section.innerHTML = paginaDespesas();
            break;
        case 'relatorio':
            section.innerHTML = paginaRelatorio();
            break;
        case 'sair':
            logout();
            renderizarPagina('login');
            break;
    }
}