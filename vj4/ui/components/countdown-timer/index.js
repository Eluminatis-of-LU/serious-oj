import _ from 'lodash';
import DOMAttachedObject from 'vj/components/DOMAttachedObject';

export default class CountdownTimer extends DOMAttachedObject {
    static DOMAttachKey = 'vjCountdownTimerInstance';

    constructor($dom, options = {}) {
      super($dom);
      this.options = {
        ...options,
      };
      this.targetDate = new Date($dom.data('end-at'));
      this.startCountDown();
    }

    startCountDown() {
      this.update();
      this.interval = setInterval(() => {
        this.update();
        const { hours, minutes, seconds } = this.calculateTimeRemaining();
        if (hours === 0 && minutes === 0 && seconds === 0) {
          this.$dom.html('Finished');
          clearInterval(this.interval);
        }
      }, 1000);
    }

    getHtml() {
      const { hours, minutes, seconds } = this.calculateTimeRemaining();
      return `${hours}:${minutes}:${seconds}`;
    }

    update() {
      const html = this.getHtml();
      this.$dom.html(html);
    }

    calculateTimeRemaining() {
      const currentDate = new Date();
      const timeRemaining = this.targetDate - currentDate;

      // Calculate days, hours, minutes, and seconds
      const hours = Math.max(0, Math.floor(timeRemaining / (1000 * 60 * 60)));
      const minutes = Math.max(0, Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60)));
      const seconds = Math.max(0, Math.floor((timeRemaining % (1000 * 60)) / 1000));

      // Return an object with the calculated values
      return {
        hours,
        minutes,
        seconds,
      };
    }
}

_.assign(CountdownTimer, DOMAttachedObject);
