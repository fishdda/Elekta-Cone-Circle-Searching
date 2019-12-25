path1 = 'C:\Users\xhuae08006\Desktop\Beijing Radiation Isocentre Acceptance Test\';
path2 = 'C:\Users\xhuae08006\Desktop\Cone\MV CENTER-154786\8pics\';
path3 = 'C:\Users\xhuae08006\Desktop\Cone\Zhongshan Unity ISO check\';
%% Cone
[circle,error] = ISOCENTER_CONE(path2);

%% Beam
% [circle_,error_] = ISOCENTER_SQUARE(path1);
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% % % % %% Read his file into matlab
% % % % [im,header]=readHISfile('C:\Users\xhuae08006\Desktop\Cone\154786(河南科技大学第一附属医院）\20190130_copy\2\G0_T0.his');
% % % % 
% % % % im_b = im2bw(im);
% % % % im_c = edge(im,'canny');
% % % % im_s = edge(im,'sobel');
% % % % im_p = edge(im,'Prewitt');
% % % % 
% % % % figure
% % % % subplot(2,2,1)
% % % % imshow(im_b,[]);
% % % % title('binary');
% % % % hold on
% % % % subplot(2,2,2)
% % % % imshow(im_c,[]);
% % % % title('canny');
% % % % hold on
% % % % subplot(2,2,3)
% % % % imshow(im_s,[]);
% % % % title('sobel');
% % % % hold on
% % % % subplot(2,2,4)
% % % % imshow(im_p,[]);
% % % % title('prewitt');
% % % % 
% % % % %% find circle with matlab inner algorithm
% % % % [centersi, radiusi,~] = imfindcircles(im,[10 20]);
% % % % [centers_bi, radius_bi,~] = imfindcircles(im_b,[10 20]);
% % % % [centers_si, radius_si,~] = imfindcircles(im_s,[10 20]);
% % % % [centers_ci, radius_ci,~] = imfindcircles(im_c,[10 20]);
% % % % [centers_pi, radius_pi,~] = imfindcircles(im_p,[10 20]);
% % % % 
% % % % [centers, radius,~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
% % % % [centers_b, radius_b,~] = imfindcircles(im_b,[80 120],'ObjectPolarity','dark');
% % % % [centers_s, radius_s,~] = imfindcircles(im_s,[80 120],'ObjectPolarity','dark');
% % % % [centers_c, radius_c,~] = imfindcircles(im_c,[80 120],'ObjectPolarity','dark');
% % % % [centers_p, radius_p,~] = imfindcircles(im_p,[80 120],'ObjectPolarity','dark');
% % % % 
% % % % 
% % % % 
% % % % 
% % % % figure
% % % % subplot(3,2,1);
% % % % imshow(im,[]);
% % % % hold on;
% % % % plot(centers(1),centers(2),'g+','LineWidth',1);
% % % % hold on;
% % % % plot(centersi(1),centersi(2),'r+','LineWidth',1);
% % % % hold on;
% % % % viscircles(centers, radius+2,'Color','g','LineWidth',0.5);
% % % % hold on;
% % % % viscircles(centersi, radiusi,'Color','r','LineWidth',0.5);
% % % % title('original');
% % % % 
% % % % hold on;
% % % % subplot(3,2,2);
% % % % imshow(im,[]);
% % % % hold on;
% % % % plot(centers_b(1),centers_b(2),'g+','LineWidth',1);
% % % % hold on;
% % % % plot(centers_bi(1),centers_bi(2),'r+','LineWidth',1);
% % % % hold on;
% % % % viscircles(centers_b, radius_b+2,'Color','g','LineWidth',0.5);
% % % % hold on;
% % % % viscircles(centers_bi, radius_bi,'Color','r','LineWidth',0.5);
% % % % title('binary');
% % % % 
% % % % hold on;
% % % % subplot(3,2,3);
% % % % imshow(im,[]);
% % % % hold on;
% % % % plot(centers_c(1),centers_c(2),'g+','LineWidth',1);
% % % % hold on;
% % % % plot(centers_ci(1),centers_ci(2),'r+','LineWidth',1);
% % % % hold on;
% % % % viscircles(centers_c, radius_c+2,'Color','g','LineWidth',0.5);
% % % % hold on;
% % % % viscircles(centers_ci, radius_ci,'Color','r','LineWidth',0.5);
% % % % title('canny');
% % % % 
% % % % hold on;
% % % % subplot(3,2,4);
% % % % imshow(im,[]);
% % % % hold on;
% % % % plot(centers_p(1),centers_p(2),'g+','LineWidth',1);
% % % % hold on;
% % % % plot(centers_pi(1),centers_pi(2),'r+','LineWidth',1);
% % % % hold on;
% % % % viscircles(centers_p, radius_p+2,'Color','g','LineWidth',0.5);
% % % % hold on;
% % % % viscircles(centers_pi, radius_pi,'Color','r','LineWidth',0.5);
% % % % title('prewitt');
% % % % 
% % % % hold on;
% % % % subplot(3,2,5);
% % % % imshow(im,[]);
% % % % hold on;
% % % % plot(centers_s(1),centers_s(2),'g+','LineWidth',1);
% % % % hold on;
% % % % plot(centers_si(1),centers_si(2),'r+','LineWidth',1);
% % % % hold on;
% % % % viscircles(centers_s, radius_s+2,'Color','g','LineWidth',0.5);
% % % % hold on;
% % % % viscircles(centers_si, radius_si,'Color','r','LineWidth',0.5);
% % % % title('sobel');
% % % % 
% % % % figure
% % % % subplot
% % % % imshow(im,[]);
% % % % hold on;
% % % % plot(centers(1),centers(2),'g+','LineWidth',0.1);
% % % % hold on;
% % % % plot(centersi(1),centersi(2),'b+','LineWidth',0.1);
% % % % hold on;
% % % % viscircles(centers, radius+2,'Color','g','LineWidth',0.1);
% % % % hold on;
% % % % viscircles(centersi, radiusi,'Color','b','LineWidth',0.1);
% % % 
% % %%
% % 
% % path = 'C:\Users\xhuae08006\Desktop\Cone\154786(河南科技大学第一附属医院）\20190130_copy\2\';
% % file = dir([path,'*.his']);
% % circle = cell(size(file,1),1);
% % 
% % figure
% % x0=0;
% % y0=0;
% % width=1500;
% % height=1000;
% % set(gcf,'position',[x0,y0,width,height])
% % ha = tight_subplot(2,4,[.01 .03],[.1 .01],[.01 .01]);
% % for i = 1:size(file,1)
% %     %% calculate center and radius
% %     disp(file(i).name)
% %     ss = strsplit(file(i).name,'.');
% %     GT = strsplit(ss{1,1},'_');
% %     Gantry = GT{1,1}(2:end);
% %     Couch = GT{1,2}(2:end);
% %     
% %     [im,~] = readHISfile([path,file(i).name]);
% %     [centerss, radiis, ~] = imfindcircles(im,[10 20]);
% %     im_b = im2bw(im);
% %     %[centersb, radiib, ~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
% % %     [centersb, radiib, ~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
% % %     if size(centersb,1) > 1
% % %         centersb = mean(centersb);
% % %         radiib = mean(radiib);
% % %     end
% %     im_b_out = zeros(1024,1024);
% %     % erase inner circle
% %     for k=1:1024
% %         for j=1:1024
% %             if sqrt((j-centerss(1))^2+(k-centerss(2))^2) < radiis+10
% %                 im_b_out(k,j) = 0;
% %             else
% %                 im_b_out(k,j) = im_b(k,j);
% %             end
% %         end
% %     end
% %     % inverse 0&1
% %     for ii=1:1024
% %         for jj=1:1024
% %             if im_b_out(ii,jj) == 0
% %                 im_b_out(ii,jj) = 1;
% %             else
% %                 im_b_out(ii,jj) = 0;
% %             end
% %         end
% %     end
% %     stats1 = regionprops('table',im_b_out,'Centroid','MajorAxisLength','MinorAxisLength');
% %     centersb = stats1.Centroid; 
% %     radiib = mean([stats1.MajorAxisLength stats1.MinorAxisLength],2)/2;
% %     if length(radiib) > 1
% %         centersb = centersb(3:end);
% %         radiib = radiib(2);
% %     end 
% % 
% %     disp(radiis);disp(radiib);
% % %     circle(i,:) = {[i,centerss,radiis,centersb,radiib]};
% %     X = (centerss(1) - centersb(1))*259/1024;
% %     Y = (centerss(2) - centersb(2))*259/1024;
% %     % Plot
% % %     subplot(2,4,i);
% %     axes(ha(i));
% %     imshow(im(350:1024-350,350:1024-350),[]);
% %     title(['Gantry:',Gantry,', Couch:',Couch])
% %     hold on;
% %     plot(centerss(1)-349,centerss(2)-349,'b+','LineWidth',1);
% %     hold on;
% %     plot(centersb(1)-349,centersb(2)-349,'g+','LineWidth',1);
% %     hold on;
% %     viscircles(centerss-349, radiis,'Color','b','LineWidth',1);
% %     hold on;
% %     viscircles(centersb-349, radiib+5,'Color','g','LineWidth',1);
% %     str = {['X:',num2str(X),'mm'],['Y:',num2str(Y),'mm']};
% %     text(2,300,str,'FontSize',10);
% % %     disp(X);
% % %     disp(Y);
% %     set(gca, 'XTickLabel', [],'XTick',[],'YTickLabel', [],'YTick',[]) 
% % 
% % end
% % set(ha(1:4),'XTickLabel',''); 
% % set(ha,'YTickLabel','')
% % % % savefig('C:\Users\xhuae08006\Desktop\Cone\results.png');
% % 
% % 
% % 
% % 
% % %% square finding
% % 
% his_path = 'C:\Users\xhuae08006\Desktop\Beijing Radiation Isocentre Acceptance Test\';
% % his_path2 = 'C:\Users\xhuae08006\Desktop\Cone\154786(河南科技大学第一附属医院）\20190130_copy\2\';
% file = dir([his_path,'*.his']);
% figure
% x0=0;
% y0=0;
% width=1500;
% height=1000;
% set(gcf,'position',[x0,y0,width,height])
% ha = tight_subplot(1,4,[.01 .03],[.1 .01],[.01 .01]);
% for i=1:size(file,1)
%     
%     disp(file(i).name)
%     ss = strsplit(file(i).name,'.');
%     GT = strsplit(ss{1,1},'_');
%     Gantry = GT{1,1}(2:end);
%     Couch = GT{1,2}(2:end);    
%     [im,~] = readHISfile([his_path,file(i).name]);
%     im_b = im2bw(im);
%     % find inner circles 
%     [centerss, radiis,~] = imfindcircles(im,[25 38]);
% %     stats = regionprops('table',im_b,'Centroid','MajorAxisLength','MinorAxisLength');
% %     centerss = stats.Centroid;
% %     radiis = mean([stats.MajorAxisLength stats.MinorAxisLength],2)/2;
% %     if length(centerss) > 1
% %         centerss = centerss(3:end);
% %         radiis = radiis(2);
% %     end
% 
%     
%     im_b_out = zeros(1024,1024);
%     % erase inner circle
%     for k=1:1024
%         for j=1:1024
%             if sqrt((j-centerss(1))^2+(k-centerss(2))^2) < radiis+10
%                 im_b_out(k,j) = 0;
%             else
%                 im_b_out(k,j) = im_b(k,j);
%             end
%         end
%     end
%     % inverse 0&1
%     for ii=1:1024
%         for jj=1:1024
%             if im_b_out(ii,jj) == 0
%                 im_b_out(ii,jj) = 1;
%             else
%                 im_b_out(ii,jj) = 0;
%             end
%         end
%     end
%     stats1 = regionprops('table',im_b_out,'Centroid','MajorAxisLength','MinorAxisLength');
%     centersb = stats1.Centroid; 
%     Width = stats1.MajorAxisLength;
%     Height = stats1.MinorAxisLength;
%     
%     
%     X = (centerss(1) - centersb(1))*259/1024;
%     Y = (centerss(2) - centersb(2))*259/1024;
%     disp(X);
%     disp(Y);
%     % Plot
% %     subplot(2,4,i);
%     axes(ha(i));
%     imshow(im,[]);
%     title(['Gantry:',Gantry,', Couch:',Couch])
%     hold on;
%     plot(centerss(1),centerss(2),'b+','LineWidth',1);
%     hold on;
%     plot(centersb(1),centersb(2),'g+','LineWidth',1);
%     hold on;
%     viscircles(centerss, radiis,'Color','b','LineWidth',1);
%     hold on;
%     rectangle('Position',[centersb(1)-Width/2,centersb(2)-Height/2,...
%         Width,Height],'EdgeColor','g');
%     str = {['Horizontal:',num2str(X),'mm'],['Vertical:',num2str(Y),'mm']};
%     text(2,300,str,'FontSize',10);
% %     disp(X);
% %     disp(Y);
%     set(gca, 'XTickLabel', [],'XTick',[],'YTickLabel', [],'YTick',[]) 
% end
% set(ha(1:4),'XTickLabel',''); 
% set(ha,'YTickLabel','')
% % 
% % %% using another methods to detect circles and squares for Cones or Beams
% % % % path = 'C:\Users\xhuae08006\Desktop\Cone\154786(河南科技大学第一附属医院）\20190130_copy\2\';
% % % % file = dir([path,'*.his']);
% % % % circle = cell(size(file,1),1);
% % % % 
% % % % figure
% % % % x0=0;
% % % % y0=0;
% % % % width=1500;
% % % % height=1000;
% % % % set(gcf,'position',[x0,y0,width,height])
% % % % ha = tight_subplot(2,4,[.01 .03],[.1 .01],[.01 .01]);
% % % % for i = 1:size(file,1)
% % % %     %% calculate center and radius
% % % %     disp(file(i).name)
% % % %     ss = strsplit(file(i).name,'.');
% % % %     GT = strsplit(ss{1,1},'_');
% % % %     Gantry = GT{1,1}(2:end);
% % % %     Couch = GT{1,2}(2:end);
% % % %     
% % % %     [im,~] = readHISfile([path,file(i).name]);
% % % % %     [centerss, radiis, ~] = imfindcircles(im,[10 20]);
% % % % %     [centersb, radiib, ~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
% % % % %     [centersb, radiib, ~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
% % % % %     if size(centersb,1) > 1
% % % % %         centersb = mean(centersb);
% % % % %         radiib = mean(radiib);
% % % % %     end
% % % % %     disp(radiis);disp(radiib);
% % % %     circle(i,:) = {[i,centerss,radiis,centersb,radiib]};
% % %     im_b = im2bw(im); % to binay image
% % % %     % find inner circles 
% % % %     stats = regionprops('table',im_b,'Centroid','MajorAxisLength','MinorAxisLength');
% % % %     centerss = stats.Centroid;
% % % %     radiis = mean([stats.MajorAxisLength stats.MinorAxisLength],2)/2;
% % % %     if length(centerss) > 1
% % % %         centerss = centerss(3:end);
% % % %         radiis = radiis(2);
% % % %     end
% % % %     % find external circles
% % %     im_b_out = zeros(1024,1024);
% % %     % erase inner circle
% % %     for k=1:1024
% % %         for j=1:1024
% % %             if sqrt((j-centerss(1))^2+(k-centerss(2))^2) < radiis+10
% % %                 im_b_out(k,j) = 0;
% % %             else
% % %                 im_b_out(k,j) = im_b(k,j);
% % %             end
% % %         end
% % %     end
% % % %     % inverse 0&1
% % %     for ii=1:1024
% % %         for jj=1:1024
% % %             if im_b_out(ii,jj) == 0
% % %                 im_b_out(ii,jj) = 1;
% % %             else
% % %                 im_b_out(ii,jj) = 0;
% % %             end
% % %         end
% % %     end
% % % %     stats1 = regionprops('table',im_b_out,'Centroid','MajorAxisLength','MinorAxisLength');
% % % %     centersb = stats1.Centroid;
% % % %     radiib = mean([stats1.MajorAxisLength stats1.MinorAxisLength],2)/2;
% % % %     if length(radiib) > 1
% % % %         centersb = centersb(3:end);
% % % %         radiib = radiib(2);
% % % %     end 
% % % %     disp(radiib);
% % % %     X = (centerss(1) - centersb(1))*259/1024;
% % % %     Y = (centerss(2) - centersb(2))*259/1024;
% % % %     % Plot
% % % % %     subplot(2,4,i);
% % % %     axes(ha(i));
% % % %     imshow(im(350:1024-350,350:1024-350),[]);
% % % %     title(['Gantry:',Gantry,', Couch:',Couch])
% % % %     hold on;
% % % %     plot(centerss(1)-349,centerss(2)-349,'b+','LineWidth',1);
% % % %     hold on;
% % % %     plot(centersb(1)-349,centersb(2)-349,'g+','LineWidth',1);
% % % %     hold on;
% % % %     viscircles(centerss-349, radiis,'Color','b','LineWidth',1);
% % % %     hold on;
% % % %     viscircles(centersb-349, radiib+10,'Color','g','LineWidth',1);
% % % %     str = {['X:',num2str(X),'mm'],['Y:',num2str(Y),'mm']};
% % % %     text(2,300,str,'FontSize',10);
% % % % %     disp(X);
% % % % %     disp(Y);
% % % %     set(gca, 'XTickLabel', [],'XTick',[],'YTickLabel', [],'YTick',[]) 
% % % % 
% % % % end
% % % % set(ha(1:4),'XTickLabel',''); 
% % % % set(ha,'YTickLabel','')