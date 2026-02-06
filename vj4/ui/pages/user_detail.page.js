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

  // Render rating chart
  const canvas = document.getElementById('rating-chart');
  if (canvas) {
    const uid = canvas.getAttribute('data-uid');
    try {
      const response = await fetch(`/user/${uid}/ratingchart`);
      const data = await response.json();

      if (data && data.length > 0) {
        const ctx = canvas.getContext('2d');
        const chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.map(d => new Date(d.date).toLocaleDateString()),
            datasets: [{
              label: 'Rating',
              data: data.map(d => d.rating),
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              tension: 0.1,
              fill: true,
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: 'Rating Chart',
              },
              tooltip: {
                callbacks: {
                  afterLabel: context => data[context.dataIndex].contest,
                },
              },
            },
            scales: {
              y: {
                beginAtZero: false,
              },
            },
          },
        });
        console.log('Rating chart rendered successfully', chart);
      }
    } catch (error) {
      console.error('Error loading rating chart:', error);
    }
  }
});

export default page;
