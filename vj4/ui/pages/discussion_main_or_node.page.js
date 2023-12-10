import { NamedPage } from 'vj/misc/PageLoader';
import CountdownTimer from 'vj/components/countdown-timer';

const page = new NamedPage('discussion_main_or_node', () => {
  CountdownTimer.getOrConstruct($('#contest-countdown-timer'));
});

export default page;
