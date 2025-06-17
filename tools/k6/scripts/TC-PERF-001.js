import http from 'k6/http';
import { check, group, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

const BASE_URL = 'http://backend:5000';
const headers = {
  'Content-Type': 'application/json',
};

export default function () {
  group('TC-PERF-001: Login with valid credentials', () => {
    const loginPayload = JSON.stringify({
      username: 'hieult',
      password: 'nec@123',
    });

    const res = http.post(`${BASE_URL}/login`, loginPayload, { headers });
    check(res, {
      'status is 200': (r) => r.status === 200,
    });
  });

  sleep(1);
}
