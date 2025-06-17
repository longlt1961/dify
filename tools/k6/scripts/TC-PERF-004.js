import http from 'k6/http';
import { check, group, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

const BASE_URL = 'http://backend:5000';

export default function () {
  group('TC-PERF-004: Get specific user by ID', () => {
    const res = http.get(`${BASE_URL}/users/1`);
    check(res, {
      'status is 200': (r) => r.status === 200,
    });
  });

  sleep(1);
}
