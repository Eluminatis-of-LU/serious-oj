import base64 from 'base-64';
import Clipboard from 'clipboard';
import { Chart, registerables } from 'chart.js';

import { NamedPage } from 'vj/misc/PageLoader';
import substitute from 'vj/utils/substitute';
import Notification from 'vj/components/notification';
import i18n from 'vj/utils/i18n';

// Register Chart.js components
Chart.register(...registerables);

const page = new NamedPage('user_detail', async () => {
  $('[name="profile_contact_copy"]').get().forEach(el => {
    const data = $(el).attr('data-content');
    const decoded = base64.decode(data);
    const clip = new Clipboard(el, { text: () => decoded });
    clip.on('success', () => {
      Notification.success(substitute(i18n('"{data}" copied to clipboard!'), { data: decoded }), 2000);
    });
    clip.on('error', () => {
      Notification.error(substitute(i18n('Copy "{data}" failed :('), { data: decoded }));
    });
  });

  // Tier ladder, low to high. Thresholds mirror RATING_RANKS in
  // vj4/model/builtin.py; colors are read from the user-rated--<slug> CSS
  // classes at runtime so the palette stays single-sourced.
  const TIER_LADDER = [
    { slug: 'novice', threshold: 0 },
    { slug: 'apprentice', threshold: 200 },
    { slug: 'specialist', threshold: 400 },
    { slug: 'expert', threshold: 600 },
    { slug: 'master', threshold: 800 },
    { slug: 'elite', threshold: 1000 },
    { slug: 'legend', threshold: 1200 },
  ];

  function readTierColors() {
    const probe = document.createElement('span');
    probe.style.display = 'none';
    document.body.appendChild(probe);
    const colors = {};
    TIER_LADDER.forEach(tier => {
      probe.className = `user-rated--${tier.slug}`;
      colors[tier.slug] = getComputedStyle(probe).color;
    });
    document.body.removeChild(probe);
    return colors;
  }

  function tierForRating(rating) {
    return TIER_LADDER.reduce(
      (match, tier) => (rating >= tier.threshold ? tier : match),
      TIER_LADDER[0],
    );
  }

  // Chart.js plugin: paint each tier as a translucent horizontal band behind
  // the line, across the full ladder.
  const tierBandsPlugin = {
    id: 'tierBands',
    beforeDatasetsDraw(chart, _args, opts) {
      const { ctx, chartArea, scales: { y } } = chart;
      const { colors } = opts;
      for (let i = 0; i < TIER_LADDER.length; i += 1) {
        const lo = TIER_LADDER[i].threshold;
        const isTopTier = i + 1 === TIER_LADDER.length;
        const yTop = isTopTier
          ? chartArea.top
          : y.getPixelForValue(Math.min(TIER_LADDER[i + 1].threshold, y.max));
        const yBottom = y.getPixelForValue(Math.max(lo, y.min));
        if (yBottom <= chartArea.top || yTop >= chartArea.bottom) continue;
        const top = Math.max(yTop, chartArea.top);
        const bottom = Math.min(yBottom, chartArea.bottom);
        ctx.save();
        ctx.fillStyle = colors[TIER_LADDER[i].slug].replace('rgb(', 'rgba(').replace(')', ', 0.12)');
        ctx.fillRect(chartArea.left, top, chartArea.right - chartArea.left, bottom - top);
        ctx.restore();
      }
    },
  };

  // Render rating chart
  const canvas = document.getElementById('rating-chart');
  if (canvas) {
    const uid = canvas.getAttribute('data-uid');
    try {
      const response = await fetch(`/user/${uid}/ratingchart`);
      const data = await response.json();

      if (data && data.length > 0) {
        const tierColors = readTierColors();
        const ratings = data.map(d => d.rating);
        const dataMin = Math.min(...ratings);
        const dataMax = Math.max(...ratings);
        // Pad the visible window so the line never hugs an edge, and snap the
        // bottom to the tier boundary the user sits above.
        const lowTier = tierForRating(dataMin);
        const yMin = Math.max(0, Math.min(lowTier.threshold, dataMin - 50));
        const yMax = dataMax + 100;

        const ctx = canvas.getContext('2d');
        const chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.map(d => new Date(d.date).toLocaleDateString()),
            datasets: [{
              label: i18n('Rating'),
              data: ratings,
              borderColor: '#444444',
              borderWidth: 2,
              pointBackgroundColor: data.map(d => tierColors[tierForRating(d.rating).slug]),
              pointBorderColor: '#ffffff',
              pointBorderWidth: 1,
              pointRadius: 4,
              pointHoverRadius: 6,
              tension: 0,
              fill: false,
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              title: {
                display: true,
                text: i18n('Rating Chart'),
              },
              tierBands: { colors: tierColors },
              tooltip: {
                callbacks: {
                  title: items => data[items[0].dataIndex].contest,
                  label: context => `${i18n('Rating')}: ${context.parsed.y}`,
                  afterBody: items => {
                    const d = data[items[0].dataIndex];
                    const sign = d.delta > 0 ? '+' : '';
                    return [
                      `${i18n('Rank')}: ${d.rank}`,
                      `${i18n('Rating Change')}: ${sign}${d.delta}`,
                    ];
                  },
                },
              },
            },
            scales: {
              y: {
                beginAtZero: false,
                min: yMin,
                max: yMax,
              },
            },
          },
          plugins: [tierBandsPlugin],
        });
        if (!chart) {
          console.error('Rating chart failed to initialise');
        }
      }
    } catch (error) {
      console.error('Error loading rating chart:', error);
    }
  }
});

export default page;
