function  circle = Find_Cir(path)

%%
% file_name = {'\1.HIS','\2.HIS','\3.HIS','\4.HIS','\5.HIS','\6.HIS','\7.HIS','\8.HIS'};
file = dir([path,'*.his']);
circle = cell(size(file,1),1);
% figure
for i = 1:size(file,1)
    %% calculate center and radius
    disp(file(i).name)
    [im,~] = readHISfile([path,file(i).name]);
    [centerss, radiis, ~] = imfindcircles(im,[10 20]);
    %[centersb, radiib, ~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
    [centersb, radiib, ~] = imfindcircles(im,[80 120],'ObjectPolarity','dark');
    if size(centersb,1) > 1
        centersb = mean(centersb);
        radiib = mean(radiib);
    end
    disp(radiis);disp(radiib);
    circle(i,:) = {[i,centerss,radiis,centersb,radiib]};
%     X = (centerss(1) - centersb(1))*260/1024;
%     Y = (centerss(2) - centersb(2))*260/1024;
    %% Plot
%     subplot(2,4,i);
%     imshow(im(300:1024-300,300:1024-300),[]);
%     hold on;
%     plot(centerss(1)-300,centerss(2)-300,'b+','LineWidth',1);
%     hold on;
%     plot(centersb(1)-300,centersb(2)-300,'g+','LineWidth',1);
%     hold on;
%     viscircles(centerss-300, radiis,'EdgeColor','b','LineWidth',0.5);
%     hold on;
%     viscircles(centersb-300, radiib,'EdgeColor','g','LineWidth',0.5);
%     disp(X);
%     disp(Y);

end
% id = circle(:,1); in_iso = circle(:,2); in_rad = circle(:,3);
% out_iso = circle(:,4); out_rad = circle(:,5);

% delta4 = {};
% for i = 1:size(error,1)
%     delta4(i,:) = {error{i,1},abs(Stand{i,2}-error{i,2}),abs(Stand{i,3}-error{i,3})};
% end 
end
