import { NamedPage } from 'vj/misc/PageLoader';
import CountdownTimer from 'vj/components/countdown-timer';

const page = new NamedPage('contest_scoreboard', () => {
  CountdownTimer.getOrConstruct($('#contest-countdown-timer'));
});

export default page;
