// Obter ID da instância da URL
function getInstanciaIdFromUrl() {
    const path = window.location.pathname;
    const parts = path.split('/');
    // URL: /instancias/{idInstancia}/detalhes/localizacao
    const idIndex = parts.indexOf('instancias') + 1;
    return parts[idIndex];
}

const idInstancia = getInstanciaIdFromUrl();

// Cores das estantes
const corMap = {
    'azul': '#3B82F6',
    'verde': '#10B981', 
    'vermelho': '#EF4444',
    'amarelo': '#F59E0B'
};

// Carregar dados da instância ao inicializar a página
document.addEventListener('DOMContentLoaded', function() {
    if (!idInstancia) {
        showError('ID da instância não fornecido');
        return;
    }
    
    carregarDetalhesInstancia();
});

async function carregarDetalhesInstancia() {
    try {
        const response = await fetch(`/instancias/${idInstancia}/detalhes`);
        if (!response.ok) {
            throw new Error('Instância não encontrada');
        }
        
        const dados = await response.json();
        exibirInformacoes(dados);
        
    } catch (error) {
        showError(error.message);
    }
}

function exibirInformacoes(dados) {
    const { instancia, livro, estante } = dados;
    
    // Determinar cor da estante
    const corEstante = corMap[estante?.cor] || '#6B7280';
    
    // Atualizar título da página
    document.title = `Localização - ${livro?.titulo || 'Livro'} | Biblioteca IoT`;
    
    // Atualizar header com cor da estante
    const header = document.getElementById('header');
    header.style.backgroundColor = corEstante;
    
    // Atualizar seta com cor da estante
    const seta = document.getElementById('setaDirecional');
    seta.style.color = corEstante;
    
    // Atualizar ícone do livro
    const bookIcon = document.getElementById('bookIcon');
    bookIcon.style.color = corEstante;
    
    // Atualizar informações do livro
    document.getElementById('livroTitulo').textContent = livro?.titulo || 'N/A';
    document.getElementById('livroAutor').textContent = livro?.autor || 'N/A';
    document.getElementById('instanciaId').textContent = instancia.idInstancia;
    document.getElementById('posicao').textContent = `${instancia.posX}m`;
    
    // Atualizar badge da estante
    const estanteBadge = document.getElementById('estanteBadge');
    estanteBadge.textContent = estante?.idEstante || 'N/A';
    estanteBadge.style.backgroundColor = corEstante;
    
    // Atualizar status
    const statusIcon = document.getElementById('statusIcon');
    statusIcon.style.color = corEstante;
    document.getElementById('situacao').textContent = instancia.situacao;
    
    // Atualizar informações da estante
    document.getElementById('estanteInfo').textContent = 
        `Estante ${estante?.idEstante || 'N/A'} - Cor ${estante?.cor?.charAt(0).toUpperCase() + estante?.cor?.slice(1) || 'N/A'}`;
    
    // Atualizar instruções
    document.getElementById('corEstante').textContent = estante?.cor || 'N/A';
    document.getElementById('posicaoEstante').textContent = `${instancia.posX}m`;
    document.getElementById('situacaoEstante').textContent = instancia.situacao;
    
    // Atualizar link de voltar
    const voltarLink = document.getElementById('voltarLink');
    voltarLink.href = `/painel/livros/${livro?.idLivro}`;
    
    // Mostrar conteúdo e esconder loading
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('content').classList.remove('hidden');
}

function showError(message) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}
