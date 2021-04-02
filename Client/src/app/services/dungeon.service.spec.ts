import { TestBed } from '@angular/core/testing';

import { DungeonService } from './dungeon.service';

describe('DungeonService', () => {
  let service: DungeonService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DungeonService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
