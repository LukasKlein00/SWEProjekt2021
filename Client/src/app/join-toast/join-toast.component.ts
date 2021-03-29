import { Component, OnInit, TemplateRef } from '@angular/core';
import { ToastService } from '../services/toast.service';

@Component({
  selector: 'app-join-toast',
  templateUrl: './join-toast.component.html',
  styleUrls: ['./join-toast.component.scss']
})
export class JoinToastComponent {
  
  constructor(public toastService: ToastService) {}

  isTemplate(toast) { return toast.textOrTpl instanceof TemplateRef; }
}
