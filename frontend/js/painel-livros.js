// frontend/js/painel-livros.js

class PainelLivros {
    constructor() {
        console.log('🏗️ Construindo PainelLivros...');
        this.livros = [];
        this.livrosFiltrados = [];
        this.termoBusca = '';
        this.ordenacao = 'titulo';
        
        this.initEventListeners();
        this.carregarLivros();
    }

    initEventListeners() {
        const form = document.getElementById('searchForm');
        const clearBtn = document.getElementById('clearBtn');
        const searchInput = document.getElementById('searchInput');
        const sortSelect = document.getElementById('sortSelect');

        // Submit do formulário
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.buscarLivros();
        });

        // Botão limpar
        clearBtn.addEventListener('click', () => {
            this.limparBusca();
        });

        // Busca em tempo real (com debounce)
        let timeoutId;
        searchInput.addEventListener('input', () => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                this.buscarLivros();
            }, 300);
        });

        // Mudança na ordenação
        sortSelect.addEventListener('change', () => {
            this.ordenacao = sortSelect.value;
            this.buscarLivros();
        });
    }

    async carregarLivros() {
        try {
            console.log('🔄 Iniciando carregamento de livros...');
            this.showLoading(true);
            
            // Tentar URL relativa primeiro
            const url = '/livros/';
            console.log('📡 Fazendo requisição para:', url);
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
            console.log('📥 Resposta recebida:', response.status, response.statusText);
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📚 Dados recebidos:', data.length, 'livros');
            
            this.livros = data;
            this.livrosFiltrados = [...this.livros];
            this.renderizarLivros();
            this.atualizarTitulo();
            console.log('✅ Livros carregados com sucesso!');
        } catch (error) {
            console.error('❌ Erro ao carregar livros:', error);
            this.mostrarErro(`Erro ao carregar os livros: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    buscarLivros() {
        const searchInput = document.getElementById('searchInput');
        const sortSelect = document.getElementById('sortSelect');
        
        this.termoBusca = searchInput.value.toLowerCase().trim();
        this.ordenacao = sortSelect.value;

        // Filtrar livros
        if (this.termoBusca === '') {
            this.livrosFiltrados = [...this.livros];
        } else {
            this.livrosFiltrados = this.livros.filter(livro => 
                livro.titulo.toLowerCase().includes(this.termoBusca) ||
                livro.autor.toLowerCase().includes(this.termoBusca)
            );
        }

        // Ordenar livros
        this.ordenarLivros();
        this.renderizarLivros();
        this.atualizarTitulo();
    }

    ordenarLivros() {
        this.livrosFiltrados.sort((a, b) => {
            if (this.ordenacao === 'id') {
                return a.idLivro.localeCompare(b.idLivro);
            } else {
                return a.titulo.localeCompare(b.titulo);
            }
        });
    }

    renderizarLivros() {
        const container = document.getElementById('livrosList');
        
        if (this.livrosFiltrados.length === 0) {
            container.innerHTML = this.renderNenhumLivro();
            return;
        }

        const livrosHtml = this.livrosFiltrados.map(livro => this.renderLivro(livro)).join('');
        container.innerHTML = livrosHtml;
        
        // Adicionar animação
        container.classList.add('fade-in');
    }

    renderLivro(livro) {
        return `
            <div class="livro-card border border-gray-200 rounded-lg p-4 lg:p-6 hover:shadow-lg transition-shadow bg-gray-50 hover:bg-white">
                <div class="flex flex-col lg:flex-row lg:justify-between lg:items-start space-y-3 lg:space-y-0">
                    <div class="flex-1">
                        <!-- Título e Autor (destaque maior) -->
                        <h3 class="text-lg lg:text-xl font-bold text-gray-900 mb-2">
                            ${this.highlightText(livro.titulo)}
                        </h3>
                        <p class="text-base lg:text-lg text-gray-700 mb-3 flex items-center">
                            <i class="fas fa-user mr-2 text-gray-500"></i>
                            ${this.highlightText(livro.autor)}
                        </p>
                        
                        <!-- Editora (destaque menor) -->
                        <p class="text-sm text-gray-600 mb-2 flex items-center">
                            <i class="fas fa-building mr-2"></i>
                            <strong>Editora:</strong> <span class="ml-1">${livro.editora}</span>
                        </p>
                        
                        <!-- Código do Livro (menor destaque) -->
                        <p class="text-xs text-gray-500 font-mono flex flex-wrap items-center gap-2 lg:gap-4">
                            <span class="flex items-center">
                                <i class="fas fa-barcode mr-1"></i>
                                <strong>ID:</strong> <span class="ml-1 break-all">${livro.idLivro}</span>
                            </span>
                            <span class="flex items-center">
                                <strong>Cutter:</strong> <span class="ml-1">${livro.codigoCutter}</span>
                            </span>
                            <span class="flex items-center">
                                <strong>Estante:</strong> <span class="ml-1">${livro.estanteId}</span>
                            </span>
                        </p>
                    </div>
                    
                    <!-- Botão Ver Detalhes -->
                    <div class="lg:ml-6 self-start lg:self-center">
                        <a 
                            href="/painel/livros/${livro.idLivro}" 
                            class="bg-blue-600 text-white px-3 py-2 lg:px-4 lg:py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center text-sm font-medium w-full lg:w-auto"
                        >
                            <i class="fas fa-eye mr-2"></i>
                            Ver Detalhes
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    renderNenhumLivro() {
        return `
            <div class="text-center py-12">
                <i class="fas fa-book-open text-6xl text-gray-300 mb-4"></i>
                <h3 class="text-xl font-semibold text-gray-600 mb-2">Nenhum livro encontrado</h3>
                <p class="text-gray-500">
                    ${this.termoBusca ? 'Tente ajustar sua busca ou limpar os filtros.' : 'Não há livros cadastrados no sistema.'}
                </p>
            </div>
        `;
    }

    highlightText(text) {
        if (!this.termoBusca) return text;
        
        const regex = new RegExp(`(${this.termoBusca})`, 'gi');
        return text.replace(regex, '<span class="search-highlight">$1</span>');
    }

    atualizarTitulo() {
        const titleElement = document.getElementById('resultsTitle');
        const countElement = document.getElementById('resultsCount');
        const searchTermElement = document.getElementById('searchTerm');

        const count = this.livrosFiltrados.length;
        const plural = count !== 1 ? 's' : '';
        
        if (this.termoBusca) {
            titleElement.textContent = 'Resultados da busca';
            searchTermElement.innerHTML = `Buscando por: "<strong>${this.termoBusca}</strong>"`;
            searchTermElement.classList.remove('hidden');
        } else {
            titleElement.textContent = 'Todos os livros';
            searchTermElement.classList.add('hidden');
        }
        
        countElement.textContent = `(${count} livro${plural})`;
    }

    limparBusca() {
        document.getElementById('searchInput').value = '';
        document.getElementById('sortSelect').value = 'titulo';
        this.termoBusca = '';
        this.ordenacao = 'titulo';
        this.livrosFiltrados = [...this.livros];
        this.ordenarLivros();
        this.renderizarLivros();
        this.atualizarTitulo();
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        const results = document.getElementById('resultsContainer');
        
        if (show) {
            loading.classList.remove('hidden');
            results.classList.add('hidden');
        } else {
            loading.classList.add('hidden');
            results.classList.remove('hidden');
        }
    }

    mostrarErro(mensagem) {
        const container = document.getElementById('livrosList');
        container.innerHTML = `
            <div class="text-center py-12">
                <i class="fas fa-exclamation-triangle text-6xl text-red-300 mb-4"></i>
                <h3 class="text-xl font-semibold text-red-600 mb-2">Erro</h3>
                <p class="text-gray-500">${mensagem}</p>
                <button onclick="location.reload()" class="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    Tentar novamente
                </button>
            </div>
        `;
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM carregado, inicializando PainelLivros...');
    new PainelLivros();
});
