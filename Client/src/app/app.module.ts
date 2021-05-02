import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import { MatSliderModule } from '@angular/material/slider';
import {MatDialogModule} from '@angular/material/dialog';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {MatBadgeModule} from '@angular/material/badge';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TestComponent } from './test/test.component';
import { ImpressumComponent } from './impressum/impressum.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { BuilderComponent } from './builder/builder.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { HomeComponent } from './home/home.component';
import { PlayComponent } from './play/play.component';
import { ChatComponent } from './chat/chat.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { CreateCharacterComponent } from './create-character/create-character.component';
import { JoinToastComponent } from './join-toast/join-toast.component';
import { ProfilComponent } from './profil/profil.component';
import { ConfirmComponent } from './confirm/confirm.component';
import { ResetComponent } from './reset/reset.component';
import { ForgotComponent } from './forgot/forgot.component';
import { ErrorComponent } from './error/error.component';


@NgModule({
  declarations: [
    AppComponent,
    TestComponent,
    ImpressumComponent,
    LoginComponent,
    RegisterComponent,
    BuilderComponent,
    HomeComponent,
    PlayComponent,
    ChatComponent,
    CreateCharacterComponent,
    JoinToastComponent,
    ProfilComponent,
    ConfirmComponent,
    ResetComponent,
    ForgotComponent,
    ErrorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgSelectModule,
    NoopAnimationsModule,
    MatSliderModule,
    MatDialogModule,
    MatSlideToggleModule,
    NgbModule,
    MatBadgeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
