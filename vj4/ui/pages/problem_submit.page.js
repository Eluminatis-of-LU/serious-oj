import { NamedPage } from 'vj/misc/PageLoader';
import CountdownTimer from 'vj/components/countdown-timer';

const page = new NamedPage(['problem_submit', 'contest_detail_problem_submit', 'homework_detail_problem_submit'], async () => {
  CountdownTimer.getOrConstruct($('#contest-countdown-timer'));
  $(document).on('click', '[name="problem-sidebar__show-category"]', ev => {
    $(ev.currentTarget).hide();
    $('[name="problem-sidebar__categories"]').show();
  });
});

export default page;
