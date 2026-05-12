// Obter dados do usuário logado (cliente ou fornecedor)
function obterClienteLogado() {
    const usuario = localStorage.getItem('usuario');
    return usuario ? usuario : null;
}

// Obter tipo de usuário (cliente ou fornecedor)
function obterTipoUsuario() {
    return localStorage.getItem('tipoUsuario');
}

// Verificar se usuário está logado
function estaLogado() {
    return localStorage.getItem('usuario') !== null;
}

// ✅ NOVA FUNÇÃO: Verificar login ao carregar a página
function verificarLogin() {
    if (estaLogado()) {
        console.log('Usuário já logado, redirecionando para layout...');
        renderizarLayout();
        return true;
    } else {
        console.log('Usuário não logado, mostrando login...');
        renderizarPagina('login');
        return false;
    }
}

function logout() {
    console.log('Fazendo logout...');
    
    // Remove todos os dados do usuário
    localStorage.removeItem('usuario');
    localStorage.removeItem('tipoUsuario');
    
    // Verifica se foi removido
    console.log('Dados após logout:', {
        usuario: localStorage.getItem('usuario'),
        tipoUsuario: localStorage.getItem('tipoUsuario')
    });
    
    // Redireciona para login
    renderizarPagina('login');
}

// Obter nome do usuário
function obterNomeUsuario() {
    const usuario = obterClienteLogado();
    return usuario ? usuario.nome : 'Usuário';
}