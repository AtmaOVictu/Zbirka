// =============================================================================
// ZAVES: Svetovna pripoved - vizualna predstavitev meje
// Koncept: Zaves je mehanizem ustvarjanja sveta (kritični-kot-in-tok.md)
// =============================================================================

import React from 'react';

interface ZavesProps {
  telegramsProcessed: number;
  isActive?: boolean;
}

/**
 * Zaves - vizualna predstavitev meje med svetom in zavestjo
 * 
 * @param telegramsProcessed - Število obdelanih telegramov (za animacijo)
 * @param isActive - Ali je zaves aktivna (tok teče)
 */
export const Zaves: React.FC<ZavesProps> = ({
  telegramsProcessed,
  isActive = true,
}) => {
  return (
    <>
      {/* Zaves - ohlapna zavesa, ki se dviga ob vsaki klasifikaciji */}
      <div
        className={`
          fixed inset-0 pointer-events-none z-0
          transition-all duration-1000 ease-out
          ${isActive ? 'opacity-100' : 'opacity-0'}
        `}
        aria-hidden="true"
      >
        {/* Gradient, ki predstavlja mejo */}
        <div
          className="absolute inset-0"
          style={{
            background: `linear-gradient(to bottom, 
              rgba(255, 255, 255, 0.05) 0%,
              rgba(255, 255, 255, 0.1) 20%,
              rgba(255, 255, 255, 0.05) 100%
            )`,
          }}
        />

        {/* Animirane črte, ki predstavljajo žške v zavesi */}
        <div
          className="absolute inset-0 overflow-hidden"
          aria-hidden="true"
        >
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="absolute w-full h-px"
              style={{
                top: `${20 + i * 15}%`,
                left: 0,
                background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
                animation: `shimmer 3s infinite ease-in-out`,
                animationDelay: `${i * 0.5}s`,
              }}
            />
          ))}
        </div>

        {/* Številka obdelanih telegramov (subtilno) */}
        <div
          className="fixed bottom-4 right-4 text-[10px] text-zinc-400"
          aria-label={`Obdelanih telegramov: ${telegramsProcessed}`}
        >
          ∂ {telegramsProcessed}
        </div>
      </div>

      {/* CSS animacija za shimmer efect */}
      <style jsx global>{{
        '@keyframes shimmer': {
          '0%, 100%': { opacity: '0.3', transform: 'translateX(-10%)' },
          '50%': { opacity: '0.7', transform: 'translateX(10%)' },
        },
      }}</style>
    </>
  );
};

export default Zaves;
