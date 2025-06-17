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
  group('TC-PERF-002: Create new user (invalid - duplicate)', () => {
    const payload = JSON.stringify({
      username: 'hieult',
      email: 'hieult@nec.vn',
      password: 'testpass123',
    });

    const res = http.post(`${BASE_URL}/users`, payload, { headers });
    check(res, {
      'status is 409 (duplicate)': (r) => r.status === 409,
    });
  });

  sleep(1);
}
