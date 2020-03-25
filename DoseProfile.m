%% read dicom dose from DICOM file
dose1_path = 'C:/Users/Public/Documents/CMS/FocalData/DCMXprtFile/monPHANTOM_TEST_Dose.dcm';
I1=dicomread(dose1_path); 
metadata = dicominfo(dose1_path);%存储信息
Dose_Cube1 = double(squeeze(I1))*metadata.DoseGridScaling;
Dose_Map1 = squeeze(Dose_Cube1(210/2,:,:));
Dose_Map1_rot = imrotate(Dose_Map1,360,'bicubic','crop');
Dose_profile1 = Dose_Map1_rot(298/2,:);

dose2_path = 'C:/Users/Public/Documents/CMS/FocalData/DCMXprtFile/monPHANTOM_TESTCollimator25_Dose.dcm';
I2=dicomread(dose2_path); 
metadata = dicominfo(dose1_path);%存储信息
Dose_Cube2 = double(squeeze(I2))*metadata.DoseGridScaling;
Dose_Map2 = squeeze(Dose_Cube2(210/2,:,:));
Dose_Map2_rot = imrotate(Dose_Map2,-25,'bicubic','crop');
Dose_profile2 = Dose_Map2_rot(298/2,:);

dose3_path = 'C:/Users/Public/Documents/CMS/FocalData/DCMXprtFile/monPHANTOM_TESTCollimator30_Dose.dcm';
I3=dicomread(dose3_path); 
metadata = dicominfo(dose1_path);%存储信息
Dose_Cube3 = double(squeeze(I3))*metadata.DoseGridScaling;
Dose_Map3 = squeeze(Dose_Cube3(210/2,:,:));
Dose_Map3_rot = imrotate(Dose_Map3,-30,'bicubic','crop');
Dose_profile3 = Dose_Map3_rot(298/2,:);

dose4_path = 'C:/Users/Public/Documents/CMS/FocalData/DCMXprtFile/monPHANTOM_TESTCollimator35_Dose.dcm';
I4=dicomread(dose4_path); 
metadata = dicominfo(dose1_path);%存储信息
Dose_Cube4 = double(squeeze(I4))*metadata.DoseGridScaling;
Dose_Map4 = squeeze(Dose_Cube4(210/2,:,:));
Dose_Map4_rot = imrotate(Dose_Map4,-35,'bicubic','crop');
Dose_profile4 = Dose_Map4_rot(298/2,:);

dose5_path = 'C:/Users/Public/Documents/CMS/FocalData/DCMXprtFile/monPHANTOM_TESTCollimator40_Dose.dcm';
I5=dicomread(dose5_path); 
metadata = dicominfo(dose1_path);%存储信息
Dose_Cube5 = double(squeeze(I5))*metadata.DoseGridScaling;
Dose_Map5 = squeeze(Dose_Cube5(210/2,:,:));
Dose_Map5_rot = imrotate(Dose_Map5,-40,'bicubic','crop');
Dose_profile5 = Dose_Map5_rot(298/2,:);

dose6_path = 'C:/Users/Public/Documents/CMS/FocalData/DCMXprtFile/monPHANTOM_TESTCollimator50_Dose.dcm';
I6=dicomread(dose6_path); 
metadata = dicominfo(dose1_path);%存储信息
Dose_Cube6 = double(squeeze(I6))*metadata.DoseGridScaling;
Dose_Map6 = squeeze(Dose_Cube6(210/2,:,:));
Dose_Map6_rot = imrotate(Dose_Map6,-50,'bicubic','crop');
Dose_profile6 = Dose_Map6_rot(298/2,:);


%% 旋转dose map来进行
% Dose_Map2_rot = imrotate(Dose_Map2,-25,'nearest','crop');
% Dose_Map3_rot = imrotate(Dose_Map3,-30,'nearest','crop');
% Dose_Map4_rot = imrotate(Dose_Map4,-35,'nearest','crop');
% 

figure;
subplot(2,2,1);
plot(1:286,Dose_profile1,'b');
hold on;
plot(1:286,Dose_profile2,'m');
hold on;
plot(1:286,Dose_profile3,'r');
hold on;
plot(1:286,Dose_profile4,'g');
hold on;
plot(1:286,Dose_profile5,'y');
hold on;
plot(1:286,Dose_profile6,'k');
xlabel('X axis'); ylabel('Gy');
legend('Collimator = 0 degree','Collimator = 25 degrees','Collimator = 30 degrees','Collimator = 35 degrees','Collimator = 40 degrees','Collimator = 50 degrees');
grid on;

subplot(2,2,2);
plot(1:298,Dose_Map1_rot(:,286/2),'b');
hold on;
plot(1:298,Dose_Map2_rot(:,286/2),'m');
hold on;
plot(1:298,Dose_Map3_rot(:,286/2),'r');
hold on;
plot(1:298,Dose_Map4_rot(:,286/2),'g');
hold on;
plot(1:298,Dose_Map5_rot(:,286/2),'y');
hold on;
plot(1:298,Dose_Map6_rot(:,286/2),'k');
xlabel('Y axis'); ylabel('Gy')
legend('Collimator = 0 degree','Collimator = 25 degrees','Collimator = 30 degrees','Collimator = 35 degrees','Collimator = 40 degrees','Collimator = 50 degrees');
grid on;

subplot(2,2,3);
plot(1:286,Dose_profile1-Dose_profile2,'g');
hold on;
plot(1:286,Dose_profile1-Dose_profile3,'y');
hold on;
plot(1:286,Dose_profile1-Dose_profile4,'r');
hold on;
plot(1:286,Dose_profile1-Dose_profile5,'b');
hold on;
plot(1:286,Dose_profile1-Dose_profile6,'m');
ylabel('profile diff');
legend('0 degree- 25 degrees','0 degrees - 30 degrees','0 degrees - 35 degrees','0 degrees - 40 degrees','0 degrees - 50 degrees');
grid on;

subplot(2,2,4);
plot(1:298,Dose_Map1_rot(:,286/2)-Dose_Map2_rot(:,286/2),'g');
hold on;
plot(1:298,Dose_Map1_rot(:,286/2)-Dose_Map3_rot(:,286/2),'y');
hold on;
plot(1:298,Dose_Map1_rot(:,286/2)-Dose_Map4_rot(:,286/2),'r');
hold on;
plot(1:298,Dose_Map1_rot(:,286/2)-Dose_Map5_rot(:,286/2),'b');
hold on;
plot(1:298,Dose_Map1_rot(:,286/2)-Dose_Map6_rot(:,286/2),'m');
ylabel('profile diff');
legend('0 degree- 25 degrees','0 degrees - 30 degrees','0 degrees - 35 degrees','0 degrees - 40 degrees','0 degrees - 50 degrees');
grid on;

%% 3D Map deviation
Map_Diff2 = Dose_Map2_rot- Dose_Map1;
Map_Diff3 = Dose_Map3_rot- Dose_Map1;
Map_Diff6 = Dose_Map6_rot- Dose_Map1;

figure;
imshow(Map_Diff6,[]);


%% 
% figure;
% plot(1:286,Dose_Map6(7:end-6,286/2)-Dose_Map1(298/2,:)','r');
