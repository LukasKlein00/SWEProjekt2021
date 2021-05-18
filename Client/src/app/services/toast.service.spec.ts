import { TestBed } from '@angular/core/testing';
import { SocketIoConfig, SocketIoModule } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';

import { ToastService } from './toast.service';

describe('ToastService', () => {
  let service: ToastService;
  const config: SocketIoConfig = { url: environment.websocketUrl, options: {} };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [SocketIoModule.forRoot(config)]
    });
    service = TestBed.inject(ToastService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
