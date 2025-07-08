let scanner = null;
let currentInstancia = null;

document.getElementById('startScanner').addEventListener('click', startScanner);
document.getElementById('stopScanner').addEventListener('click', stopScanner);
document.getElementById('confirmarEmprestimo').addEventListener('click', confirmarEmprestimo);

function startScanner() {
    // Verificar se estamos em HTTPS ou localhost (necessário para iOS)
    if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
        showError('Para usar a câmera no iPhone, o site precisa estar em HTTPS');
        return;
    }

    document.getElementById('scanner-container').classList.remove('hidden');
    document.getElementById('startScanner').classList.add('hidden');
    
    // Detectar tipo de dispositivo para otimização
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const isAndroid = /Android/.test(navigator.userAgent);
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    // Configuração otimizada baseada no dispositivo
    let config;
    
    if (isIOS) {
        // Configuração específica para iOS (mais conservadora)
        config = {
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#scanner'),
                constraints: {
                    width: 640,
                    height: 480,
                    facingMode: "environment",
                    aspectRatio: 4/3,
                    frameRate: { ideal: 15, max: 30 }
                }
            },
            locator: {
                patchSize: "medium",
                halfSample: true
            },
            numOfWorkers: 1,
            frequency: 5,
            decoder: {
                readers: [
                    "code_128_reader", 
                    "code_39_reader",
                    "ean_reader", 
                    "ean_8_reader"
                ]
            },
            locate: true
        };
    } else if (isAndroid) {
        // Configuração específica para Android (mais agressiva)
        config = {
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#scanner'),
                constraints: {
                    width: { min: 480, ideal: 720, max: 1280 },
                    height: { min: 320, ideal: 540, max: 720 },
                    facingMode: "environment",
                    aspectRatio: { ideal: 1.33333 },
                    focusMode: "continuous",
                    exposureMode: "continuous"
                }
            },
            locator: {
                patchSize: "medium",
                halfSample: false
            },
            numOfWorkers: 2,
            frequency: 8,
            decoder: {
                readers: [
                    "code_128_reader", 
                    "code_39_reader",
                    "ean_reader", 
                    "ean_8_reader"
                ]
            },
            locate: true
        };
    } else {
        // Configuração para desktop (padrão original)
        config = {
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#scanner'),
                constraints: {
                    width: 640,
                    height: 480,
                    facingMode: "environment",
                    aspectRatio: 4/3
                }
            },
            locator: {
                patchSize: "medium",
                halfSample: false
            },
            numOfWorkers: 2,
            frequency: 10,
            decoder: {
                readers: [
                    "code_128_reader", 
                    "ean_reader", 
                    "ean_8_reader", 
                    "code_39_reader",
                    "code_39_vin_reader"
                ]
            },
            locate: true
        };
    }
    
    console.log('Dispositivo detectado:', { isIOS, isAndroid, isMobile });
    console.log('Configuração aplicada:', config);

    Quagga.init(config, function(err) {
        if (err) {
            console.error('Erro ao inicializar câmera:', err);
            
            // Mensagens de erro específicas por dispositivo
            let errorMessage = 'Erro ao acessar a câmera';
            
            switch(err.name) {
                case 'NotAllowedError':
                    errorMessage = isIOS ? 
                        'Permissão de câmera negada. Vá em Configurações > Safari > Câmera e permita o acesso.' :
                        'Permissão de câmera negada. Permita o acesso à câmera nas configurações do navegador.';
                    break;
                case 'NotFoundError':
                    errorMessage = 'Câmera não encontrada neste dispositivo.';
                    break;
                case 'NotSupportedError':
                    errorMessage = 'Câmera não suportada neste navegador.';
                    break;
                case 'OverconstrainedError':
                    errorMessage = 'Configurações de câmera não suportadas. Tentando configuração mais simples...';
                    // Tentar configuração de fallback
                    tryFallbackConfig();
                    return;
                default:
                    if (isMobile) {
                        errorMessage += '. Tente usar Chrome ou Safari e certifique-se de que as permissões estão habilitadas.';
                    }
                    break;
            }
            
            showError(errorMessage);
            stopScanner();
            return;
        }
        
        console.log('Câmera inicializada com sucesso para:', isMobile ? 'Mobile' : 'Desktop');
        Quagga.start();
    });

    Quagga.onDetected(function(data) {
        const code = data.codeResult.code;
        const format = data.codeResult.format;
        
        console.log('=== DEBUG SCANNER EMPRÉSTIMO ===');
        console.log('Código detectado:', code);
        console.log('Formato:', format);
        console.log('Tamanho:', code.length);
        console.log('Dispositivo:', isMobile ? 'Mobile' : 'Desktop');
        console.log('==============================');
        
        // Vibração otimizada por dispositivo
        if (navigator.vibrate) {
            if (isIOS) {
                navigator.vibrate([100, 50, 100]); // Padrão diferente para iOS
            } else {
                navigator.vibrate(200);
            }
        }
        
        stopScanner();
        buscarInstancia(code);
    });
}

function stopScanner() {
    if (Quagga) {
        Quagga.stop();
    }
    document.getElementById('scanner-container').classList.add('hidden');
    document.getElementById('startScanner').classList.remove('hidden');
}

async function buscarInstancia(idInstancia) {
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch(`/instancias/${idInstancia}`);
        if (!response.ok) {
            throw new Error('Instância não encontrada');
        }
        
        const instancia = await response.json();
        
        // Buscar dados do livro
        const livroResponse = await fetch(`/livros/${instancia.idLivro}`);
        const livro = await livroResponse.json();
        
        currentInstancia = instancia;
        exibirInformacoes(instancia, livro);
        
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function exibirInformacoes(instancia, livro) {
    document.getElementById('livroTitulo').textContent = livro.titulo;
    document.getElementById('livroAutor').textContent = livro.autor;
    document.getElementById('livroEditora').textContent = livro.editora;
    document.getElementById('livroEstante').textContent = livro.estanteId;
    document.getElementById('instanciaId').textContent = instancia.idInstancia;
    
    const situacaoElement = document.getElementById('instanciaSituacao');
    situacaoElement.textContent = instancia.situacao.toUpperCase();
    
    // Aplicar cor baseada na situação
    situacaoElement.className = 'px-2 py-1 rounded text-xs font-medium ';
    if (instancia.situacao === 'disponivel') {
        situacaoElement.className += 'bg-green-100 text-green-800';
    } else if (instancia.situacao === 'emprestado') {
        situacaoElement.className += 'bg-yellow-100 text-yellow-800';
    } else {
        situacaoElement.className += 'bg-red-100 text-red-800';
    }
    
    document.getElementById('livroInfo').classList.remove('hidden');
}

async function confirmarEmprestimo() {
    if (!currentInstancia) return;
    
    showLoading(true);
    
    try {
        const response = await fetch(`/instancias/${currentInstancia.idInstancia}/emprestar`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erro ao emprestar livro');
        }
        
        document.getElementById('livroInfo').classList.add('hidden');
        document.getElementById('sucesso').classList.remove('hidden');
        
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

// Função de fallback para dispositivos com limitações
function tryFallbackConfig() {
    console.log('Tentando configuração de fallback...');
    
    const fallbackConfig = {
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#scanner'),
            constraints: {
                width: 320,
                height: 240,
                facingMode: "environment"
            }
        },
        locator: {
            patchSize: "small",
            halfSample: true
        },
        numOfWorkers: 1,
        frequency: 3,
        decoder: {
            readers: ["code_128_reader", "code_39_reader"]
        },
        locate: true
    };
    
    Quagga.init(fallbackConfig, function(err) {
        if (err) {
            console.error('Fallback também falhou:', err);
            showError('Não foi possível inicializar a câmera mesmo com configurações básicas: ' + err.message);
            stopScanner();
            return;
        }
        
        console.log('Câmera inicializada com configuração de fallback');
        Quagga.start();
    });
}
