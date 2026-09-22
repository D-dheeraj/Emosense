// 4-7-8 Guided Breathing Visualizer Module
class BreathingVisualizer {
  constructor() {
    this.phaseText = document.getElementById('breathingPhase');
    this.timerText = document.getElementById('breathingTimer');
    this.ring = document.getElementById('breathingRing');
    this.startBtn = document.getElementById('startBreathingBtn');

    this.isRunning = false;
    this.timerInterval = null;
    this.currentCycle = 0;
    this.totalCycles = 4;

    if (this.startBtn) {
      this.startBtn.addEventListener('click', () => this.toggle());
    }
  }

  toggle() {
    if (this.isRunning) {
      this.stop();
    } else {
      this.start();
    }
  }

  start() {
    this.isRunning = true;
    this.currentCycle = 0;
    this.startBtn.innerHTML = '<i class="fa-solid fa-square"></i> Stop Reset';
    this.startBtn.style.background = 'linear-gradient(135deg, var(--accent-rose), #dc2626)';
    this.runCycle();
  }

  stop() {
    this.isRunning = false;
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.phaseText.textContent = 'Click Start to Begin';
    this.timerText.textContent = '04';
    this.ring.className = 'breathing-circle-inner';
    this.startBtn.innerHTML = '<i class="fa-solid fa-play"></i> Start 4-7-8 Reset';
    this.startBtn.style.background = 'linear-gradient(135deg, var(--accent-emerald), #059669)';
  }

  runCycle() {
    if (!this.isRunning || this.currentCycle >= this.totalCycles) {
      this.phaseText.textContent = 'Session Complete! Feel the Calm.';
      this.stop();
      return;
    }

    this.currentCycle++;
    // Phase 1: Inhale 4s
    this.runPhase('Inhale Slowly...', 4, 'inhale', () => {
      if (!this.isRunning) return;
      // Phase 2: Hold 7s
      this.runPhase('Hold Breath...', 7, 'hold', () => {
        if (!this.isRunning) return;
        // Phase 3: Exhale 8s
        this.runPhase('Exhale Completely...', 8, 'exhale', () => {
          if (!this.isRunning) return;
          this.runCycle();
        });
      });
    });
  }

  runPhase(text, seconds, cssClass, onComplete) {
    this.phaseText.textContent = `${text} (Cycle ${this.currentCycle}/${this.totalCycles})`;
    this.ring.className = `breathing-circle-inner ${cssClass}`;

    let remaining = seconds;
    this.timerText.textContent = remaining < 10 ? `0${remaining}` : `${remaining}`;

    if (this.timerInterval) clearInterval(this.timerInterval);

    this.timerInterval = setInterval(() => {
      remaining--;
      if (remaining >= 0) {
        this.timerText.textContent = remaining < 10 ? `0${remaining}` : `${remaining}`;
      } else {
        clearInterval(this.timerInterval);
        if (onComplete) onComplete();
      }
    }, 1000);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.breathingVisualizer = new BreathingVisualizer();
});
