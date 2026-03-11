// Simple Working Mouse Cursor Effects

class SimpleCursorEffects {
  constructor() {
    this.cursor = null;
    this.follower = null;
    this.isTouch = false;
    this.mouseX = 0;
    this.mouseY = 0;
    
    this.init();
  }

  init() {
    // Check for touch device
    this.isTouch = ('ontouchstart' in window || navigator.maxTouchPoints > 0);
    
    if (this.isTouch) {
      console.log('Touch device detected - cursor effects disabled');
      return;
    }
    
    console.log('Desktop detected - initializing cursor effects');
    this.createCursors();
    this.bindEvents();
    this.animate();
  }

  createCursors() {
    // Create main cursor
    this.cursor = document.createElement('div');
    this.cursor.className = 'custom-cursor';
    this.cursor.style.left = '0px';
    this.cursor.style.top = '0px';
    document.body.appendChild(this.cursor);

    // Create follower
    this.follower = document.createElement('div');
    this.follower.className = 'cursor-follower';
    this.follower.style.left = '0px';
    this.follower.style.top = '0px';
    document.body.appendChild(this.follower);
    
    // Activate custom cursor
    document.body.classList.add('cursor-active');
    
    console.log('Cursor elements created and activated');
  }

  animate() {
    let followerX = 0;
    let followerY = 0;
    
    const updateFollower = () => {
      // Smooth following animation
      followerX += (this.mouseX - followerX) * 0.1;
      followerY += (this.mouseY - followerY) * 0.1;
      
      if (this.follower) {
        this.follower.style.left = followerX + 'px';
        this.follower.style.top = followerY + 'px';
      }
      
      requestAnimationFrame(updateFollower);
    };
    
    updateFollower();
  }

  bindEvents() {
    // Mouse move
    document.addEventListener('mousemove', (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
      
      if (this.cursor) {
        this.cursor.style.left = this.mouseX + 'px';
        this.cursor.style.top = this.mouseY + 'px';
      }
      
      // Random particles
      if (Math.random() > 0.9) {
        this.createParticle(this.mouseX, this.mouseY);
      }
    });

    // Click effects
    document.addEventListener('mousedown', (e) => {
      if (this.cursor) {
        this.cursor.classList.add('click');
      }
      this.createRipple(e.clientX, e.clientY);
    });

    document.addEventListener('mouseup', () => {
      if (this.cursor) {
        this.cursor.classList.remove('click');
      }
    });

    // Hover effects
    this.setupHoverEffects();
    
    // Window events
    document.addEventListener('mouseleave', () => {
      if (this.cursor) this.cursor.style.opacity = '0';
      if (this.follower) this.follower.style.opacity = '0';
    });
    
    document.addEventListener('mouseenter', () => {
      if (this.cursor) this.cursor.style.opacity = '1';
      if (this.follower) this.follower.style.opacity = '1';
    });
  }

  setupHoverEffects() {
    // Button hover effects
    const buttons = document.querySelectorAll(
      'button, .btn, .confident-btn-primary, .book-analysis-btn, .nav-cta-btn'
    );
    
    buttons.forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        if (this.cursor) this.cursor.classList.add('hover', 'button');
        if (this.follower) this.follower.classList.add('hover');
      });
      
      btn.addEventListener('mouseleave', () => {
        if (this.cursor) this.cursor.classList.remove('hover', 'button');
        if (this.follower) this.follower.classList.remove('hover');
      });
    });

    // Text hover effects
    const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6');
    textElements.forEach(el => {
      el.addEventListener('mouseenter', () => {
        if (this.cursor) this.cursor.classList.add('text');
      });
      
      el.addEventListener('mouseleave', () => {
        if (this.cursor) this.cursor.classList.remove('text');
      });
    });
  }

  createParticle(x, y) {
    const particle = document.createElement('div');
    particle.className = 'cursor-particle';
    particle.style.left = x + 'px';
    particle.style.top = y + 'px';
    document.body.appendChild(particle);
    
    setTimeout(() => {
      if (particle.parentNode) {
        particle.remove();
      }
    }, 1000);
  }

  createRipple(x, y) {
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    ripple.style.left = (x - 50) + 'px';
    ripple.style.top = (y - 50) + 'px';
    ripple.style.width = '100px';
    ripple.style.height = '100px';
    document.body.appendChild(ripple);
    
    setTimeout(() => {
      if (ripple.parentNode) {
        ripple.remove();
      }
    }, 600);
  }

  setToothCursor() {
    if (this.cursor) {
      this.cursor.classList.add('tooth');
    }
  }

  resetCursor() {
    if (this.cursor) {
      this.cursor.classList.remove('tooth');
    }
  }
}

// Initialize when page loads
let cursorEffects = null;

function initCursor() {
  console.log('Initializing cursor effects...');
  cursorEffects = new SimpleCursorEffects();
  
  // Add toggle button for desktop only
  if (!cursorEffects.isTouch) {
    createToothButton();
  }
}

function createToothButton() {
  const button = document.createElement('button');
  button.innerHTML = '🦷';
  button.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: white;
    border: 2px solid #4A90E2;
    font-size: 18px;
    cursor: pointer;
    z-index: 100000;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
    transition: all 0.3s ease;
  `;
  
  let isToothMode = false;
  button.addEventListener('click', () => {
    if (cursorEffects) {
      if (isToothMode) {
        cursorEffects.resetCursor();
        button.innerHTML = '🦷';
        button.style.background = 'white';
      } else {
        cursorEffects.setToothCursor();
        button.innerHTML = '🖱️';
        button.style.background = '#4A90E2';
        button.style.color = 'white';
      }
      isToothMode = !isToothMode;
    }
  });
  
  document.body.appendChild(button);
}

// Initialize immediately if DOM is ready, otherwise wait
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCursor);
} else {
  initCursor();
}

  createParticle(x, y) {
    const particle = document.createElement('div');
    particle.className = 'cursor-particle';
    particle.style.transform = `translate(${x - 3}px, ${y - 3}px)`;
    
    document.body.appendChild(particle);

    // Remove particle after animation with cleanup
    setTimeout(() => {
      if (particle.parentNode) {
        particle.remove();
      }
    }, 1200);
  }

  createRipple(x, y) {
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    ripple.style.transform = `translate(${x - 50}px, ${y - 50}px)`;
    ripple.style.width = '100px';
    ripple.style.height = '100px';
    
    document.body.appendChild(ripple);

    // Remove ripple after animation with cleanup
    setTimeout(() => {
      if (ripple.parentNode) {
        ripple.remove();
      }
    }, 600);
  }

  // Toggle different cursor styles
  setToothCursor() {
    if (this.cursor) {
      this.cursor.classList.add('tooth-cursor');
    }
  }

  resetCursor() {
    if (this.cursor) {
      this.cursor.classList.remove('tooth-cursor');
    }
  }

  // Cleanup method
  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    
    if (this.cursor) this.cursor.remove();
    if (this.follower) this.follower.remove();
    if (this.glow) this.glow.remove();
    
    document.body.classList.remove('cursor-effects-active');
  }
}

// Initialize cursor effects when DOM is loaded
let cursorEffects = null;

function initializeCursorEffects() {
  if (cursorEffects) {
    cursorEffects.destroy();
  }
  
  cursorEffects = new PerfectCursorEffects();
  
  // Add tooth cursor toggle button only on desktop
  if (!cursorEffects.isTouch) {
    createToggleButton();
  }
}

function createToggleButton() {
  // Remove existing button if any
  const existingBtn = document.querySelector('.cursor-toggle-btn');
  if (existingBtn) {
    existingBtn.remove();
  }
  
  const toothToggle = document.createElement('button');
  toothToggle.className = 'cursor-toggle-btn';
  toothToggle.innerHTML = '🦷';
  toothToggle.setAttribute('aria-label', 'Toggle tooth cursor');
  toothToggle.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border: 2px solid #4A90E2;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    cursor: pointer;
    z-index: 100000;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  `;
  
  toothToggle.addEventListener('mouseenter', () => {
    toothToggle.style.transform = 'scale(1.1)';
    toothToggle.style.boxShadow = '0 6px 20px rgba(74, 144, 226, 0.3)';
  });
  
  toothToggle.addEventListener('mouseleave', () => {
    toothToggle.style.transform = 'scale(1)';
    toothToggle.style.boxShadow = '0 4px 12px rgba(74, 144, 226, 0.2)';
  });
  
  let toothMode = false;
  toothToggle.addEventListener('click', () => {
    if (cursorEffects) {
      if (toothMode) {
        cursorEffects.resetCursor();
        toothToggle.innerHTML = '🦷';
        toothToggle.style.background = 'white';
      } else {
        cursorEffects.setToothCursor();
        toothToggle.innerHTML = '🖱️';
        toothToggle.style.background = '#4A90E2';
        toothToggle.style.color = 'white';
      }
      toothMode = !toothMode;
    }
  });
  
  document.body.appendChild(toothToggle);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeCursorEffects);
} else {
  initializeCursorEffects();
}

// Re-initialize on page navigation (for SPAs)
window.addEventListener('load', initializeCursorEffects);