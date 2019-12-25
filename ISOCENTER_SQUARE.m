function [circle,error] = ISOCENTER_SQUARE(path)
%% 
% This program is aimed to detect isocenter of circle,square regardless of
% the size of Cone,Beam field. As a benchmark, RIT could provide a much 
% better and dependent final results condering commercial use.

%% 
file = dir([path,'*.his']);
circle = cell(size(file,1),1);
error = cell(size(file,1),1);
%%
file = dir([path,'*.his']);
figure
x0=0;
y0=0;
width=1500;
height=1000;
set(gcf,'position',[x0,y0,width,height]);
ha = tight_subplot(size(file,1)/4,4,[.01 .03],[.1 .01],[.01 .01]);  
for i = 1:size(file,1)
    
    %% read his file detect inner circles
    [im,~] = readHISfile([path,file(i).name]);

    %% utlizing regionprops to detect inner circle
    im_b = im2bw(im); % convert to binary images
    stats = regionprops('table',im_b,'Centroid',...
        'MajorAxisLength','MinorAxisLength'); % find circle center and radius
    center = stats.Centroid;  % calculate center
    radii = mean([stats.MajorAxisLength stats.MinorAxisLength],2)/2;
    if length(radii) > 1
        centerss = center(3:4);
        radiis = radii(end);
    end
    disp(radiis)
    %% hough transformation to do secondary check
    lower_rad = int16(radiis-8); upper_rad = int16(radiis+5);
    [centerss_2, radiis_2, ~] = imfindcircles(im,[lower_rad upper_rad]);
    if length(radiis_2) > 1
        disp('2 inner circles');
        centerss_2 = mean(centerss_2);
        radiis_2 = mean(radiis_2);
    end
    
    disp(['hough circle:',num2str(centerss_2(1)),',',num2str(centerss_2(2))]);
    disp(['regionprops circle:',num2str(centerss(1)),',',num2str(centerss(2))]);
    
    %% judge and check select which circle
    if abs(mean(centerss-centerss_2)) < 0.01
        center_in = (centerss_2+centerss)./2;
        radius_in = (radiis_2+radiis)/2;
    else 
        center_in = centerss_2;
        radius_in = radiis_2;
    end
    
    %% find external square 
    im_b_out = zeros(1024,1024);
    % erase inner circle
    for k=1:1024
        for j=1:1024
            if sqrt((j-centerss(1))^2+(k-centerss(2))^2) < radiis+10
                im_b_out(k,j) = 0;
            else
                im_b_out(k,j) = im_b(k,j);
            end
        end
    end
    % inverse 0&1
    for ii=1:1024
        for jj=1:1024
            if im_b_out(ii,jj) == 0
                im_b_out(ii,jj) = 1;
            else
                im_b_out(ii,jj) = 0;
            end
        end
    end
    stats1 = regionprops('table',im_b_out,'Centroid',...
        'MajorAxisLength','MinorAxisLength');
    centersb = stats1.Centroid; 
    Width = stats1.MajorAxisLength;
    Height = stats1.MinorAxisLength;
%     disp(['external circle radius:',num2str(centersb(1)),',',num2str(centersb(2))]);
    %% using hough circle as secondary check for external circles
%     [center_hough, rad_hough, ~] = imfindcircles(im,[int16(radiib-10) int16(radiib+10)],'ObjectPolarity','dark');
%     disp(['hough external circle radius:',num2str(center_hough(1)),',',num2str(center_hough(2))]);
    
    %% calculate errors
    circle(i,:) = {[i,center_in,radius_in,centersb]};
    
    X = (center_in(1) - centersb(1))*259/1024;
    Y = (center_in(2) - centersb(2))*259/1024;
    error(i,:) = {[X,Y]};
    disp(['horizontal:',num2str(X),'mm']);
    disp(['vertical:',num2str(Y),'mm']);
    
    
    %% determine the gantry angles & couch angles
    ss = strsplit(file(i).name,'.');
    GT = strsplit(ss{1,1},'_');
    Gantry = GT{1,1}(2:end);
    Couch = GT{1,2}(2:end);
    %% plot the figure
    axes(ha(i));
    imshow(im,[]);
    title(['Gantry:',Gantry,', Couch:',Couch])
    hold on;
    plot(center_in(1),center_in(2),'b+','LineWidth',2);
    hold on;
    plot(centersb(1),centersb(2),'g+','LineWidth',1);
    hold on;
    viscircles(center_in, radius_in,'Color','b','LineWidth',1);
    hold on;
    rectangle('Position',[centersb(1)-Width/2,centersb(2)-Height/2,...
        Width,Height],'EdgeColor','g');
    str = {['Horizontal:',num2str(X),'mm'],['Vertical:',num2str(Y),'mm']};
    text(2,300,str,'FontSize',10);
    set(gca, 'XTickLabel', [],'XTick',[],'YTickLabel', [],'YTick',[]);   
end
set(ha(1:4),'XTickLabel',''); 
set(ha,'YTickLabel','');
saveas(gcf,[path,'show.png'])
end