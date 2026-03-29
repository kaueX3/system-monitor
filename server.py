           -ms-user-select: text !important;
       }
       
        /* Gradiente de fundo preto com detalhes roxos */
        /* Gradiente de fundo preto limpo */
       .gradient-bg {
           position: fixed;
           top: 0;
           left: 0;
           width: 100%;
           height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(147, 51, 234, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(124, 58, 237, 0.08) 0%, transparent 50%),
                linear-gradient(135deg, #000000 0%, #0a0014 25%, #000000 50%, #0a0014 75%, #000000 100%);
            background-size: 200% 200%, 200% 200%, 200% 200%, 100% 100%;
            animation: gradientShift 25s ease infinite;
            opacity: 0.9;
            background: #000000;
            opacity: 1;
           z-index: 0;
       }
       
       @keyframes gradientShift {
            0% { background-position: 0% 50%, 100% 50%, 50% 100%, 0% 50%; }
            25% { background-position: 50% 0%, 0% 100%, 100% 0%, 50% 0%; }
            50% { background-position: 100% 50%, 50% 0%, 0% 50%, 100% 50%; }
            75% { background-position: 50% 100%, 100% 0%, 50% 100%, 50% 100%; }
            100% { background-position: 0% 50%, 100% 50%, 50% 100%, 0% 50%; }
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
       }
       
        /* Sistema de partículas avançado */
        /* Partículas mínimas e escuras */
       .particles {
           position: fixed;
           top: 0;
@@ -650,635 +641,282 @@ def after_request(response):
       .particle {
           position: absolute;
           border-radius: 50%;
            animation: float 30s infinite linear;
            animation: float 40s infinite linear;
       }
       
       .particle.small {
            width: 2px;
            height: 2px;
            background: rgba(147, 51, 234, 0.8);
            box-shadow: 0 0 8px rgba(147, 51, 234, 0.6);
            width: 1px;
            height: 1px;
            background: rgba(76, 29, 149, 0.3);
            box-shadow: 0 0 3px rgba(76, 29, 149, 0.2);
       }
       
       .particle.medium {
            width: 4px;
            height: 4px;
            background: rgba(139, 92, 246, 0.7);
            box-shadow: 0 0 12px rgba(139, 92, 246, 0.5);
            width: 2px;
            height: 2px;
            background: rgba(76, 29, 149, 0.2);
            box-shadow: 0 0 4px rgba(76, 29, 149, 0.1);
       }
       
       .particle.large {
            width: 6px;
            height: 6px;
            background: rgba(124, 58, 237, 0.6);
            box-shadow: 0 0 16px rgba(124, 58, 237, 0.4);
            width: 3px;
            height: 3px;
            background: rgba(76, 29, 149, 0.15);
            box-shadow: 0 0 5px rgba(76, 29, 149, 0.1);
       }
       
       @keyframes float {
           0% { transform: translateY(100vh) rotate(0deg) scale(0); opacity: 0; }
            10% { opacity: 1; transform: scale(1); }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) rotate(1080deg) scale(0); opacity: 0; }
            10% { opacity: 0.3; transform: scale(1); }
            90% { opacity: 0.3; }
            100% { transform: translateY(-100vh) rotate(720deg) scale(0); opacity: 0; }
       }
       
        /* Grid hexagonal animado sutil */
        /* Remover grid hexagonal */
       .hex-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(30deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(150deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(30deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(150deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(60deg, rgba(139, 92, 246, 0.02) 25%, transparent 25.5%, transparent 75%, rgba(139, 92, 246, 0.02) 75%, rgba(139, 92, 246, 0.02)),
                linear-gradient(60deg, rgba(139, 92, 246, 0.02) 25%, transparent 25.5%, transparent 75%, rgba(139, 92, 246, 0.02) 75%, rgba(139, 92, 246, 0.02));
            background-size: 80px 140px;
            background-position: 0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px;
            animation: hexMove 15s linear infinite;
            z-index: 1;
        }
        
        @keyframes hexMove {
            0% { background-position: 0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px; }
            100% { background-position: 80px 0, 80px 0, 120px 70px, 120px 70px, 80px 0, 120px 70px; }
            display: none;
       }
       
        /* Container principal com glassmorphism preto */
        /* Container principal clean */
       .login-container {
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(25px) saturate(180%);
            border-radius: 35px;
            padding: 60px;
            max-width: 500px;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 50px;
            max-width: 450px;
           width: 100%;
            border: 2px solid rgba(147, 51, 234, 0.3);
            border: 1px solid rgba(76, 29, 149, 0.2);
           box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.8),
                0 0 100px rgba(147, 51, 234, 0.15),
                inset 0 1px 0 rgba(147, 51, 234, 0.1),
                inset 0 -1px 0 rgba(0, 0, 0, 0.5);
                0 10px 30px rgba(0, 0, 0, 0.8),
                0 0 20px rgba(76, 29, 149, 0.1);
           position: relative;
           z-index: 10;
            animation: containerEntrance 1.2s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center;
            animation: containerEntrance 0.8s ease-out;
       }
       
       @keyframes containerEntrance {
            0% { 
            from { 
               opacity: 0; 
                transform: translateY(100px) scale(0.8) rotateX(15deg); 
                filter: blur(20px);
                transform: translateY(30px) scale(0.95); 
           }
            50% {
                opacity: 0.8;
                transform: translateY(-20px) scale(1.05) rotateX(0deg);
                filter: blur(5px);
            }
            100% { 
            to { 
               opacity: 1; 
                transform: translateY(0) scale(1) rotateX(0deg); 
                filter: blur(0px);
                transform: translateY(0) scale(1); 
           }
       }
       
        /* Aura animada ao redor do container */
        /* Borda sutil */
       .login-container::before {
           content: '';
           position: absolute;
            top: -3px;
            left: -3px;
            right: -3px;
            bottom: -3px;
            top: -1px;
            left: -1px;
            right: -1px;
            bottom: -1px;
           background: linear-gradient(
               45deg, 
                rgba(147, 51, 234, 0.8), 
                rgba(139, 92, 246, 0.6), 
                rgba(124, 58, 237, 0.4), 
                rgba(109, 40, 217, 0.3), 
                rgba(91, 33, 182, 0.2), 
                rgba(76, 29, 149, 0.1),
                rgba(147, 51, 234, 0.8)
                rgba(76, 29, 149, 0.3), 
                rgba(76, 29, 149, 0.1), 
                rgba(76, 29, 149, 0.3)
           );
            border-radius: 35px;
            border-radius: 20px;
           z-index: -1;
            opacity: 0.7;
            animation: borderAura 4s ease-in-out infinite;
            background-size: 300% 300%;
        }
        
        @keyframes borderAura {
            0%, 100% { 
                opacity: 0.6; 
                filter: blur(15px) brightness(1.2);
                background-position: 0% 50%;
            }
            50% { 
                opacity: 1; 
                filter: blur(0px) brightness(1.5);
                background-position: 100% 50%;
            }
            opacity: 0.5;
       }
       
        /* Logo com animações cinematográficas */
        /* Logo clean */
       .logo {
           text-align: center;
            margin-bottom: 45px;
            position: relative;
            animation: logoFloat 4s ease-in-out infinite;
        }
        
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.02); }
            margin-bottom: 35px;
       }
       
       .logo h1 {
            font-size: 4em;
            font-weight: 900;
            background: linear-gradient(
                135deg, 
                #9333ea 0%, 
                #8b5cf6 20%, 
                #7c3aed 40%, 
                #6d28d9 60%, 
                #5b21b6 80%, 
                #4c1d95 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 
                0 0 80px rgba(147, 51, 234, 1),
                0 0 120px rgba(139, 92, 246, 0.6);
            letter-spacing: 4px;
            margin-bottom: 15px;
            animation: textGlow 3s ease-in-out infinite alternate;
            position: relative;
        }
        
        @keyframes textGlow {
            from { 
                filter: brightness(1.2) drop-shadow(0 0 30px rgba(147, 51, 234, 1));
                transform: scale(1);
            }
            to { 
                filter: brightness(1.5) drop-shadow(0 0 50px rgba(147, 51, 234, 1.2));
                transform: scale(1.05);
            }
        }
        
        /* Partículas ao redor do logo */
        .logo-particles {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200%;
            height: 200%;
            pointer-events: none;
        }
        
        .logo-particle {
            position: absolute;
            width: 3px;
            height: 3px;
            background: #9333ea;
            border-radius: 50%;
            animation: orbitParticle 6s linear infinite;
            box-shadow: 0 0 10px rgba(147, 51, 234, 0.8);
        }
        
        @keyframes orbitParticle {
            0% { transform: rotate(0deg) translateX(100px) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: rotate(360deg) translateX(100px) rotate(-360deg); opacity: 0; }
            font-size: 3.5em;
            font-weight: 800;
            color: #4c1d95;
            letter-spacing: 3px;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(76, 29, 149, 0.3);
       }
       
       .logo p {
            color: #a78bfa;
            font-size: 1.2em;
            font-weight: 300;
            letter-spacing: 3px;
            color: #6b21a8;
            font-size: 1em;
            font-weight: 400;
            letter-spacing: 2px;
           text-transform: uppercase;
            opacity: 0.9;
            text-shadow: 0 0 30px rgba(167, 139, 250, 0.8);
            animation: subtitlePulse 2s ease-in-out infinite alternate;
            opacity: 0.8;
       }
       
        @keyframes subtitlePulse {
            from { opacity: 0.7; transform: scale(1); }
            to { opacity: 1; transform: scale(1.05); }
        /* Remover partículas do logo */
        .logo-particles {
            display: none;
       }
       
        /* Formulário com efeitos holográficos */
        /* Formulário clean */
       .form-group {
            margin-bottom: 30px;
            margin-bottom: 25px;
           position: relative;
       }
       
       .form-group label {
           display: block;
            margin-bottom: 15px;
            color: #e9d5ff;
            font-weight: 600;
            font-size: 0.95em;
            margin-bottom: 10px;
            color: #6b21a8;
            font-weight: 500;
            font-size: 0.9em;
           text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            text-shadow: 0 0 15px rgba(233, 213, 255, 0.5);
            letter-spacing: 1px;
       }
       
       .form-group input {
           width: 100%;
            padding: 22px 25px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid rgba(147, 51, 234, 0.2);
            border-radius: 20px;
            padding: 18px 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(76, 29, 149, 0.2);
            border-radius: 12px;
           color: #fff;
            font-size: 1.1em;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            backdrop-filter: blur(10px);
            font-size: 1em;
            transition: all 0.3s ease;
       }
       
       .form-group input:focus {
           outline: none;
            border-color: #9333ea;
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 
                0 0 40px rgba(147, 51, 234, 0.6),
                0 0 80px rgba(147, 51, 234, 0.3),
                inset 0 1px 0 rgba(147, 51, 234, 0.3);
            transform: translateY(-3px) scale(1.02);
            border-color: #4c1d95;
            background: rgba(0, 0, 0, 0.9);
            box-shadow: 0 0 15px rgba(76, 29, 149, 0.2);
       }
       
       .form-group input::placeholder {
           color: #6b7280;
            transition: all 0.3s ease;
        }
        
        .form-group input:focus::placeholder {
            opacity: 0.3;
            transform: translateX(5px);
       }
       
        /* Efeito de onda ao digitar */
        /* Remover efeitos extras */
       .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(147, 51, 234, 0.3);
            transform: scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
            display: none;
       }
       
        @keyframes rippleEffect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        .input-glow {
            display: none;
       }
       
        /* Botão premium com animações cinematográficas */
        /* Botão clean */
       .login-btn {
           width: 100%;
            padding: 24px;
            padding: 20px;
           background: linear-gradient(
               135deg, 
                #9333ea 0%, 
                #8b5cf6 25%, 
                #7c3aed 50%, 
                #6d28d9 75%, 
                #5b21b6 100%
                #4c1d95 0%, 
                #6b21a8 50%, 
                #7c3aed 100%
           );
           border: none;
            border-radius: 20px;
            border-radius: 12px;
           color: #fff;
            font-size: 1.3em;
            font-weight: 800;
            font-size: 1.1em;
            font-weight: 600;
           cursor: pointer;
           text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 25px;
            position: relative;
            overflow: hidden;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 10px 40px rgba(147, 51, 234, 0.5),
                0 0 80px rgba(147, 51, 234, 0.3);
        }
        
        /* Efeito de brilho passando pelo botão */
        .login-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg, 
                transparent, 
                rgba(255, 255, 255, 0.4), 
                transparent
            );
            transition: left 0.8s ease;
        }
        
        .login-btn::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                45deg, 
                transparent 30%, 
                rgba(255, 255, 255, 0.1) 50%, 
                transparent 70%
            );
            transform: translateX(-100%);
            transition: transform 0.6s ease;
            letter-spacing: 2px;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(76, 29, 149, 0.2);
       }
       
       .login-btn:hover {
            transform: translateY(-5px) scale(1.03);
            box-shadow: 
                0 15px 50px rgba(147, 51, 234, 0.7),
                0 0 100px rgba(147, 51, 234, 0.4);
        }
        
        .login-btn:hover::before {
            left: 100%;
        }
        
        .login-btn:hover::after {
            transform: translateX(100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(76, 29, 149, 0.3);
       }
       
       .login-btn:active {
            transform: translateY(-2px) scale(1.01);
            transform: translateY(0);
       }
       
        /* Estados de loading avançados */
       .login-btn.loading {
            animation: btnLoading 2s infinite;
            animation: btnPulse 1.5s infinite;
           pointer-events: none;
       }
       
        @keyframes btnLoading {
            0%, 100% { 
                transform: scale(1); 
                background: linear-gradient(135deg, #7c3aed, #6d28d9, #5b21b6);
            }
            25% { 
                transform: scale(1.05); 
                background: linear-gradient(135deg, #8b5cf6, #7c3aed, #6d28d9);
            }
            50% { 
                transform: scale(1.02); 
                background: linear-gradient(135deg, #9333ea, #8b5cf6, #7c3aed);
            }
            75% { 
                transform: scale(1.05); 
                background: linear-gradient(135deg, #a855f7, #9333ea, #8b5cf6);
            }
        @keyframes btnPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
       }
       
        /* Mensagens com animações premium */
        /* Mensagens clean */
       .message {
           text-align: center;
            margin-top: 40px;
            padding: 30px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            border-left: 4px solid #9333ea;
            backdrop-filter: blur(15px);
            animation: messageEntrance 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .message::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #9333ea, transparent);
            animation: messageScan 3s linear infinite;
        }
        
        @keyframes messageScan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        @keyframes messageEntrance {
            from { 
                opacity: 0; 
                transform: translateY(30px) scale(0.9); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            border-left: 3px solid #4c1d95;
       }
       
       .message p {
            color: #c4b5fd;
            color: #9ca3af;
           font-style: italic;
            line-height: 1.9;
            font-size: 1em;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 1;
            line-height: 1.6;
            font-size: 0.9em;
       }
       
       .error, .success {
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
           text-align: center;
            font-weight: 600;
            font-weight: 500;
           display: none;
            animation: alertSlide 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        @keyframes alertSlide {
            from { 
                opacity: 0; 
                transform: translateY(-30px) scale(0.8); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
       }
       
       .error {
            background: rgba(127, 29, 29, 0.2);
            border: 2px solid rgba(239, 68, 68, 0.4);
            background: rgba(127, 29, 29, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
           color: #fca5a5;
            box-shadow: 
                0 0 30px rgba(239, 68, 68, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
       }
       
       .success {
            background: rgba(20, 83, 45, 0.2);
            border: 2px solid rgba(34, 197, 94, 0.4);
            background: rgba(20, 83, 45, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
           color: #86efac;
            box-shadow: 
                0 0 30px rgba(34, 197, 94, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
       }
       
        /* Indicadores de digitação avançados */
        /* Remover indicadores de digitação */
       .typing-indicator {
            position: absolute;
            right: 25px;
            top: 50%;
            transform: translateY(-50%);
           display: none;
            gap: 3px;
        }
        
        .typing-indicator.active {
            display: flex;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: linear-gradient(135deg, #9333ea, #8b5cf6);
            animation: typingBounce 1.2s infinite;
            box-shadow: 0 0 10px rgba(147, 51, 234, 0.5);
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingBounce {
            0%, 60%, 100% { 
                transform: translateY(0) scale(1); 
                opacity: 1;
            }
            30% { 
                transform: translateY(-12px) scale(1.2); 
                opacity: 0.8;
            }
        }
        
        /* Efeito de brilho nos inputs */
        .input-glow {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 20px;
            background: linear-gradient(45deg, transparent, rgba(147, 51, 234, 0.2), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .form-group input:focus + .input-glow {
            opacity: 1;
            animation: inputGlow 2s ease-in-out infinite;
        }
        
        @keyframes inputGlow {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.8; }
       }
       
       /* Responsive design */
       @media (max-width: 480px) {
           .login-container {
                padding: 40px 30px;
                padding: 30px 25px;
               margin: 20px;
           }
           
           .logo h1 {
                font-size: 3em;
                font-size: 2.8em;
           }
           
           .form-group input {
                padding: 18px 20px;
                padding: 16px 18px;
           }
           
           .login-btn {
                padding: 20px;
                font-size: 1.1em;
                padding: 18px;
                font-size: 1em;
           }
       }
       
        /* Animações de sucesso */
        /* Remover animações complexas */
       .success-animation {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100px;
            height: 100px;
            pointer-events: none;
            z-index: 9999;
            display: none;
       }
       
       .success-circle {
            width: 100%;
            height: 100%;
            border: 3px solid #22c55e;
            border-radius: 50%;
            animation: successCircle 1s ease-out;
        }
        
        @keyframes successCircle {
            0% { 
                transform: scale(0); 
                opacity: 1;
            }
            50% {
                transform: scale(1.2);
                opacity: 0.8;
            }
            100% { 
                transform: scale(1.5); 
                opacity: 0;
            }
            display: none;
       }
       
       .success-checkmark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 40px;
            height: 40px;
            animation: checkmarkAppear 0.5s ease-out 0.3s both;
        }
        
        @keyframes checkmarkAppear {
            0% { 
                transform: translate(-50%, -50%) scale(0) rotate(-45deg); 
                opacity: 0;
            }
            100% { 
                transform: translate(-50%, -50%) scale(1) rotate(0deg); 
                opacity: 1;
            }
            display: none;
       }
   </style>
</head>
@@ -1329,39 +967,25 @@ def after_request(response):
   </div>

   <script>
        // Criar partículas avançadas
        function createAdvancedParticles() {
        // Criar partículas mínimas
        function createMinimalParticles() {
           const particlesContainer = document.getElementById('particles');
            const particleCount = 80;
            const particleCount = 20;
           
           for (let i = 0; i < particleCount; i++) {
               const particle = document.createElement('div');
               const size = Math.random() > 0.7 ? 'large' : Math.random() > 0.4 ? 'medium' : 'small';
               particle.className = `particle ${size}`;
               particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 25 + 's';
                particle.style.animationDuration = (20 + Math.random() * 15) + 's';
                particle.style.animationDelay = Math.random() * 40 + 's';
                particle.style.animationDuration = (30 + Math.random() * 20) + 's';
               particlesContainer.appendChild(particle);
           }
       }
       
        // Criar partículas orbitais do logo
        function createLogoParticles() {
            const logoParticles = document.getElementById('logoParticles');
            const particleCount = 8;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'logo-particle';
                particle.style.animationDelay = (i * 0.75) + 's';
                logoParticles.appendChild(particle);
            }
        }
        
        // Prevenir seleção de texto em toda a página
        // Prevenir seleção de texto
       function preventSelection() {
           document.addEventListener('selectstart', function(e) {
                // Permitir seleção apenas em inputs
               if (!e.target.matches('input, input *')) {
                   e.preventDefault();
               }
@@ -1374,24 +998,10 @@ def after_request(response):
           document.addEventListener('contextmenu', function(e) {
               e.preventDefault();
           });
            
            // Prevenir cópia com Ctrl+C
            document.addEventListener('keydown', function(e) {
                if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
                    const selection = window.getSelection();
                    const selectedText = selection.toString();
                    
                    // Permitir cópia apenas de inputs
                    if (!selection.anchorNode || !selection.anchorNode.parentElement || !selection.anchorNode.parentElement.matches('input')) {
                        e.preventDefault();
                    }
                }
            });
       }
       
        // Inicializar partículas e proteção
        createAdvancedParticles();
        createLogoParticles();
        // Inicializar
        createMinimalParticles();
       preventSelection();
       
       // Elementos do formulário
@@ -1402,79 +1012,8 @@ def after_request(response):
       const successMsg = document.getElementById('successMsg');
       const usernameInput = document.getElementById('username');
       const passwordInput = document.getElementById('password');
        const usernameTyping = document.getElementById('usernameTyping');
        const passwordTyping = document.getElementById('passwordTyping');
        
        // Efeito de ripple nos inputs
        function createRipple(element, event) {
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            
            const rect = element.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = event.clientX - rect.left - size / 2;
            const y = event.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            element.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        }
        
        // Efeitos de digitação avançados
        usernameInput.addEventListener('input', function(e) {
            if (this.value.length > 0) {
                this.style.borderColor = '#9333ea';
                this.style.boxShadow = '0 0 30px rgba(147, 51, 234, 0.5)';
                usernameTyping.classList.add('active');
                setTimeout(() => usernameTyping.classList.remove('active'), 1200);
                
                // Efeito de brilho progressivo
                const progress = Math.min(this.value.length / 10, 1);
                this.style.background = `rgba(45, 27, 105, ${0.4 + progress * 0.2})`;
            } else {
                this.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                this.style.boxShadow = 'none';
                this.style.background = 'rgba(26, 0, 51, 0.6)';
            }
        });
        
        passwordInput.addEventListener('input', function(e) {
            if (this.value.length > 0) {
                this.style.borderColor = '#9333ea';
                this.style.boxShadow = '0 0 30px rgba(147, 51, 234, 0.5)';
                passwordTyping.classList.add('active');
                setTimeout(() => passwordTyping.classList.remove('active'), 1200);
                
                // Efeito de brilho progressivo
                const progress = Math.min(this.value.length / 10, 1);
                this.style.background = `rgba(45, 27, 105, ${0.4 + progress * 0.2})`;
            } else {
                this.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                this.style.boxShadow = 'none';
                this.style.background = 'rgba(26, 0, 51, 0.6)';
            }
        });
        
        // Efeito de ripple ao clicar nos inputs
        [usernameInput, passwordInput].forEach(input => {
            input.addEventListener('click', function(e) {
                createRipple(this.parentElement, e);
            });
            
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.03)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
       
        // Envio do formulário com animações cinematográficas
        // Envio do formulário simplificado
       loginForm.addEventListener('submit', async (e) => {
           e.preventDefault();
           
@@ -1485,186 +1024,45 @@ def after_request(response):
           errorMsg.style.display = 'none';
           successMsg.style.display = 'none';
           
            // Estado de loading avançado
            // Estado de loading
           loginBtn.classList.add('loading');
           btnText.textContent = 'VERIFICANDO...';
           loginBtn.disabled = true;
           
            // Adicionar efeito de pulsação no container
            document.querySelector('.login-container').style.animation = 'containerPulse 1s ease-in-out';
            
            // Simular verificação com animação
            // Simular verificação
           setTimeout(() => {
               if (username === 'lealdade' && password === 'lealdade') {
                    // Sucesso espetacular
                    successMsg.textContent = '✨ Acesso concedido! Bem-vindo ao portal exclusivo...';
                    // Sucesso
                    successMsg.textContent = '✓ Acesso concedido! Redirecionando...';
                   successMsg.style.display = 'block';
                   
                    // Mudar cor do botão para sucesso
                    loginBtn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a, #15803d)';
                    btnText.textContent = '✓ ACESSO LIBERADO';
                    
                    // Criar animação de sucesso
                    createSuccessAnimation();
                    loginBtn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
                    btnText.textContent = 'ACESSO LIBERADO';
                   
                    // Efeito de confete avançado
                    createAdvancedConfetti();
                    
                    // Redirecionar após 3 segundos
                    // Redirecionar após 2 segundos
                   setTimeout(() => {
                        document.querySelector('.login-container').style.animation = 'containerExit 1s ease-in forwards';
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 800);
                    }, 3000);
                        window.location.href = '/dashboard';
                    }, 2000);
               } else {
                    // Erro dramático
                    errorMsg.textContent = '❌ Credenciais inválidas! Acesso negado ao sistema.';
                    // Erro
                    errorMsg.textContent = '✗ Credenciais inválidas! Tente novamente.';
                   errorMsg.style.display = 'block';
                   
                    // Resetar botão com animação
                   loginBtn.classList.remove('loading');
                    btnText.textContent = 'ACESSO NEGADO';
                    loginBtn.style.background = 'linear-gradient(135deg, #dc2626, #b91c1c, #991b1b)';
                    
                    // Efeito de shake dramático
                    document.querySelector('.login-container').style.animation = 'dramaticShake 0.8s ease-out';
                    btnText.textContent = 'TENTAR NOVAMENTE';
                    loginBtn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                   
                   setTimeout(() => {
                        loginBtn.style.background = 'linear-gradient(135deg, #9333ea, #8b5cf6, #7c3aed)';
                        btnText.textContent = 'TENTAR NOVAMENTE';
                        loginBtn.style.background = 'linear-gradient(135deg, #4c1d95, #6b21a8, #7c3aed)';
                        btnText.textContent = 'ENTRAR';
                       loginBtn.disabled = false;
                        document.querySelector('.login-container').style.animation = '';
                    }, 2500);
                    }, 2000);
                   
                   // Limpar senha e focar
                   passwordInput.value = '';
                   passwordInput.focus();
                    
                    // Efeito de erro nos inputs
                    [usernameInput, passwordInput].forEach(input => {
                        input.style.borderColor = '#dc2626';
                        input.style.boxShadow = '0 0 30px rgba(220, 38, 38, 0.5)';
                        setTimeout(() => {
                            input.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                            input.style.boxShadow = 'none';
                        }, 2000);
                    });
               }
            }, 2500);
        });
        
        // Animação de confete avançado
        function createAdvancedConfetti() {
            const colors = ['#9333ea', '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', '#22c55e', '#16a34a'];
            const confettiCount = 50;
            
            for (let i = 0; i < confettiCount; i++) {
                const confetti = document.createElement('div');
                confetti.style.position = 'fixed';
                confetti.style.width = Math.random() * 12 + 8 + 'px';
                confetti.style.height = confetti.style.width;
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.top = '-20px';
                confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0%';
                confetti.style.zIndex = '9999';
                confetti.style.pointerEvents = 'none';
                confetti.style.boxShadow = `0 0 10px ${confetti.style.background}`;
                document.body.appendChild(confetti);
                
                // Animação de queda realista
                const duration = 2000 + Math.random() * 1500;
                const rotation = Math.random() * 720;
                const sway = (Math.random() - 0.5) * 200;
                
                confetti.animate([
                    { 
                        transform: 'translateY(0) translateX(0) rotate(0deg) scale(0)', 
                        opacity: 0 
                    },
                    { 
                        transform: 'translateY(20vh) translateX(0) rotate(180deg) scale(1)', 
                        opacity: 1,
                        offset: 0.1
                    },
                    { 
                        transform: `translateY(100vh) translateX(${sway}px) rotate(${rotation}deg) scale(0.8)`, 
                        opacity: 0.8,
                        offset: 0.9
                    },
                    { 
                        transform: `translateY(110vh) translateX(${sway * 1.5}px) rotate(${rotation}deg) scale(0)`, 
                        opacity: 0 
                    }
                ], {
                    duration: duration,
                    easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                });
                
                setTimeout(() => confetti.remove(), duration);
            }
        }
        
        // Animação de sucesso
        function createSuccessAnimation() {
            const successDiv = document.createElement('div');
            successDiv.className = 'success-animation';
            successDiv.innerHTML = `
                <div class="success-circle"></div>
                <svg class="success-checkmark" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="3">
                    <path d="M5 12l5 5L20 7"/>
                </svg>
            `;
            document.body.appendChild(successDiv);
            
            setTimeout(() => successDiv.remove(), 1500);
        }
        
        // Adicionar animações CSS dinâmicas
        const dynamicStyles = document.createElement('style');
        dynamicStyles.textContent = `
            @keyframes containerPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.02); }
            }
            
            @keyframes dramaticShake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
                20%, 40%, 60%, 80% { transform: translateX(8px); }
            }
            
            @keyframes containerExit {
                0% { 
                    opacity: 1; 
                    transform: scale(1) rotateX(0deg); 
                    filter: blur(0px);
                }
                100% { 
                    opacity: 0; 
                    transform: scale(0.8) rotateX(15deg); 
                    filter: blur(20px);
                }
            }
        `;
        document.head.appendChild(dynamicStyles);
        
        // Efeito de hover no logo
        document.querySelector('.logo').addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.05)';
        });
        
        document.querySelector('.logo').addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Efeito parallax sutil no mouse move
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 20;
            const y = (e.clientY / window.innerHeight - 0.5) * 20;
            
            document.querySelector('.login-container').style.transform = `translateX(${x}px) translateY(${y}px)`;
            }, 1500);
       });
   </script>
</body>
