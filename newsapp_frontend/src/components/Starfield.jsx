import React, { useEffect, useRef } from 'react';

const Starfield = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    // Resize canvas to match window size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Create stars
    const stars = [];
    const numStars = Math.floor((window.innerWidth * window.innerHeight) / 1500); // Density

    for (let i = 0; i < numStars; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5,
        alpha: Math.random(),
        speed: (Math.random() * 0.02) + 0.005, // Twinkle speed
        direction: Math.random() > 0.5 ? 1 : -1,
        color: Math.random() > 0.8 ? '#86fc88' : '#ffffff' // Occasional green tint
      });
    }

    // Animation loop
    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < stars.length; i++) {
        const star = stars[i];

        // Update alpha for twinkling effect
        star.alpha += star.speed * star.direction;
        if (star.alpha >= 1) {
          star.alpha = 1;
          star.direction = -1;
        } else if (star.alpha <= 0.1) {
          star.alpha = 0.1;
          star.direction = 1;
        }

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        
        // Convert hex to rgb for rgba
        const r = star.color === '#ffffff' ? 255 : 134;
        const g = star.color === '#ffffff' ? 255 : 252;
        const b = star.color === '#ffffff' ? 255 : 136;
        
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${star.alpha})`;
        ctx.fill();
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0,
        pointerEvents: 'none'
      }}
    />
  );
};

export default Starfield;
