import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import { MatSliderModule } from '@angular/material/slider';

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
    ChatComponent
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
